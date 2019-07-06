# Import built-in modules
import wx
import wx.ribbon
from wx.ribbon import RibbonButtonBar
import wx.lib.agw.ribbon as RB

import os
import pickle
import copy

from wx.lib.docview import CommandProcessor

# Import project modules
from .dialogs.dlg_split_task import SplitTaskDialog
from .dialogs.dlg_move_task_segment import MoveTaskSegmentDialog
from .dialogs.dlg_project_information import ProjectInformationDialog
from core.task import Task
from core.project import Project
from constants import *
from .gantt_chart.status import *
from .commands.add_task import AddTaskCommand
from .commands.remove_task import RemoveTaskCommand
from .commands.move_task_up import MoveTaskUpCommand
from .commands.move_task_down import MoveTaskDownCommand
from .commands.merge_task_segments import MergeTaskSegments
from gui.accelerators import *


class Ribbon(RB.RibbonBar):
    ribbon_buttons = []
    project = None
    task_index = None
    command_processor = None
    ribbon_button_bar_event = RB.EVT_RIBBONBUTTONBAR_CLICKED

    class IDS:
        # -----------
        ADD_TASK = 100
        DELETE_TASK = 101
        INDENT_TASK = 102
        OUTDENT_TASK = 103
        # -----------
        SPLIT_TASK = 200
        MERGE_SEGMENTS = 201
        RENAME_TASK = 202
        MOVE_SEGMENT = 203
        MOVE_UP = 204
        MOVE_DOWN = 205
        UNDO = 206
        REDO = 207
        # -----------
        NEW_PROJECT = 300
        OPEN_PROJECT = 301
        SAVE_PROJECT = 302
        SAVE_AS_PROJECT = 303
        # -----------
        PROJECT_INFORMATION = 401
        PROJECT_SETTINGS = 402

    RIBBON_BUTTON_SIZE = (24, 24)

    def __init__(self, parent, project, wbs):
        super().__init__(parent=parent,
                         agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE|RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
        self.create_pages()
        self.set_button_cursors()

        self.parent = parent

        self.command_processor: CommandProcessor = self.parent.command_processor

        self.project = project

        self.wbs = wbs

        # Bindings
        self.Bind(wx.EVT_MENU, self.on_undo, id=AcceleratorIds.CTRL_Z)
        self.Bind(wx.EVT_MENU, self.on_redo, id=AcceleratorIds.CTRL_Y)
        self.Bind(wx.EVT_MENU, self.on_delete_task, id=AcceleratorIds.CTRL_SHIFT_DEL)
        self.Bind(wx.EVT_MENU, self.on_add_task, id=AcceleratorIds.CTRL_SHIFT_PLUS)
        self.Bind(wx.EVT_MENU, self.on_save_project, id=AcceleratorIds.CTRL_S)
        self.Bind(wx.EVT_MENU, self.on_open_project, id=AcceleratorIds.CTRL_O)
        self.Bind(wx.EVT_MENU, self.on_new_project, id=AcceleratorIds.CTRL_N)
        self.Bind(wx.EVT_MENU, self.on_split_task, id=AcceleratorIds.CTRL_T)
        self.Bind(wx.EVT_MENU, self.on_move_segment, id=AcceleratorIds.CTRL_SHIFT_S)
        self.Bind(wx.EVT_MENU, self.on_merge_segments, id=AcceleratorIds.CTRL_M)

        self.SetAcceleratorTable(accelerator_table)
        art_provider: wx.lib.agw.ribbon.art_msw.RibbonMSWArtProvider = self.GetArtProvider()
        primary = wx.Colour(132, 172, 200, 255)
        secondary = wx.Colour(128, 222, 234, 255)
        tertiary = wx.Colour(128, 222, 234, 125)
        art_provider.SetColourScheme(primary, secondary, tertiary)

    def create_pages(self):
        self.page_project()
        self.page_gantt_chart()
        # self.page_scurve()
        # self.Realize()

    # --------------
    # Pages
    # --------------
    def page_project(self):
        project_page = RB.RibbonPage(self, wx.ID_ANY, 'Project')
        self.panel_project_file(project_page)
        self.panel_project_properties(project_page)

    def page_gantt_chart(self):
        # ---------------- GANTT CHART PAGE ---------------- #
        gantt_page = RB.RibbonPage(self, label='Gantt Chart')
        self.panel_gantt_basic(gantt_page)
        self.panel_gantt_edit(gantt_page)

    def page_scurve(self):
        # ---------------- GANTT CHART PAGE ---------------- #

        scurve_page = RB.RibbonPage(self, label='S-Curve')

        scurve_panel = wx.Panel(parent=scurve_page)
        scurve_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        btn1 = wx.Button(parent=scurve_panel, label='SCurve Button')
        scurve_page_sizer.Add(btn1, pos=(0, 0))

        scurve_panel.SetSizer(scurve_page_sizer)

    # --------------
    # Ribbon Panels
    # --------------
    def panel_project_properties(self, page):
        project_properties_panel = RB.RibbonPanel(page, wx.ID_ANY, 'PROPERTIES', wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        project_properties_sizer = wx.BoxSizer(wx.VERTICAL)

        tb = RB.RibbonButtonBar(project_properties_panel, wx.ID_ANY)
        tb.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        project_properties_sizer.Add(tb, 0, wx.EXPAND)

        icon_information = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                                  'ribbon', 'gantt', 'project_information.png'))
        tb.AddSimpleButton(self.IDS.PROJECT_INFORMATION, 'Project Information', icon_information,
                     'Project basic information.')

        icon_settings = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                               'ribbon', 'gantt', 'project_settings.png'))
        tb.AddSimpleButton(self.IDS.PROJECT_SETTINGS, 'Settings', icon_settings, 'Project Settings')

        self.Bind(self.ribbon_button_bar_event, self.on_project_information_clicked, id=self.IDS.PROJECT_INFORMATION)

        tb.Realize()

        project_properties_panel.SetSizer(project_properties_sizer)

    def panel_project_file(self, page):
        # -- File Panel -- #
        project_file_panel = RB.RibbonPanel(page, wx.ID_ANY, 'FILE', wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        project_general_sizer = wx.BoxSizer(wx.VERTICAL)

        tb = RB.RibbonButtonBar(project_file_panel)
        tb.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        project_general_sizer.Add(tb, 0, wx.EXPAND)

        # New project
        icon_new_project = wx.ArtProvider.GetBitmap(wx.ART_NEW, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.NEW_PROJECT, 'New Project', icon_new_project, 'Create new project.')
        self.Bind(self.ribbon_button_bar_event, self.on_new_project, id=self.IDS.NEW_PROJECT)

        # Open project
        icon_open_project = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.OPEN_PROJECT, 'Open Project', icon_open_project, 'Open a project file.')
        self.Bind(self.ribbon_button_bar_event, self.on_open_project, id=self.IDS.OPEN_PROJECT)

        # Save project
        icon_save_project = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.SAVE_PROJECT, 'Save Project', icon_save_project, 'Save project file.')
        self.Bind(self.ribbon_button_bar_event, self.on_save_project, id=self.IDS.SAVE_PROJECT)

        # Save as project
        icon_save_project_as = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.SAVE_AS_PROJECT, 'Save Project as',
                     icon_save_project_as, 'Save project as new file.')
        self.Bind(self.ribbon_button_bar_event, self.on_save_project_as, id=self.IDS.SAVE_AS_PROJECT)

        tb.Realize()

        project_file_panel.SetSizer(project_general_sizer)

    def panel_gantt_basic(self, page):
        # -- Task Panel -- #
        gantt_task_panel = RB.RibbonPanel(page, wx.ID_ANY, 'BASIC', wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        gantt_page_sizer = wx.BoxSizer(wx.VERTICAL)

        tb = RB.RibbonButtonBar(gantt_task_panel)
        tb.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        gantt_page_sizer.Add(tb, 0, wx.EXPAND)

        # Add task button
        icon_add_task = wx.ArtProvider.GetBitmap(wx.ART_PLUS, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.ADD_TASK, 'Add New Task', icon_add_task, 'Add new task to the project.')
        self.Bind(self.ribbon_button_bar_event, self.on_add_task, id=self.IDS.ADD_TASK)

        # Delete task button
        icon_delete_task = self.get_stock_bitmap(wx.ART_MINUS, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.DELETE_TASK, 'Delete Task', icon_delete_task, 'Remove the selected task from project.')
        self.Bind(self.ribbon_button_bar_event, self.on_delete_task, id=self.IDS.DELETE_TASK)

        # tb.Add()

        # Outdent task button
        icon_outdent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.OUTDENT_TASK, 'Outdent Task', icon_outdent_task,
                     'Remove the task from the immediate parent.')
        self.Bind(self.ribbon_button_bar_event, self.on_outdent_task, id=self.IDS.OUTDENT_TASK)

        # Indent task button
        icon_indent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, size=self.RIBBON_BUTTON_SIZE)
        tb.AddSimpleButton(self.IDS.INDENT_TASK, 'Indent Task', icon_indent_task, 'Set the above task as parent.')
        self.Bind(self.ribbon_button_bar_event, self.on_indent_task, id=self.IDS.INDENT_TASK)

        tb.Realize()

        gantt_task_panel.SetSizer(gantt_page_sizer)
        # -- End Task Panel -- #

    def panel_gantt_edit(self, page):
        panel = RB.RibbonPanel(page, wx.ID_ANY, 'EDIT', wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        tb = RB.RibbonButtonBar(panel)
        tb.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tb, 0, wx.EXPAND)

        icon_split = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                            'ribbon', 'gantt', 'split.png'))
        tb.AddSimpleButton(self.IDS.SPLIT_TASK, 'Split Task', icon_split, 'Split a task segment.')
        self.Bind(self.ribbon_button_bar_event, self.on_split_task, id=self.IDS.SPLIT_TASK)

        icon_merge = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                            'ribbon', 'gantt', 'merge.png'))
        tb.AddSimpleButton(self.IDS.MERGE_SEGMENTS, 'Merge Task Segments', icon_merge, 'Merge all task segments.')
        self.Bind(self.ribbon_button_bar_event, self.on_merge_segments, id=self.IDS.MERGE_SEGMENTS)

        icon_edit_start = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                                 'ribbon', 'gantt', 'edit_start.png'))
        tb.AddSimpleButton(self.IDS.MOVE_SEGMENT, 'Move Task Segment', icon_edit_start,
                     'Move the task segment start.')
        self.Bind(self.ribbon_button_bar_event, self.on_move_segment, id=self.IDS.MOVE_SEGMENT)

        icon_move_up = wx.ArtProvider.GetBitmap(wx.ART_GO_UP)
        tb.AddSimpleButton(self.IDS.MOVE_UP, 'Move Up', icon_move_up,
                     'Move a task up by one row.')
        self.Bind(self.ribbon_button_bar_event, self.on_task_move_up, id=self.IDS.MOVE_UP)

        icon_move_down = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN)
        tb.AddSimpleButton(self.IDS.MOVE_DOWN, 'Move Down', icon_move_down,
                     'Move a task down by one row.')
        self.Bind(self.ribbon_button_bar_event, self.on_task_move_down, id=self.IDS.MOVE_DOWN)

        icon_undo = wx.ArtProvider.GetBitmap(wx.ART_UNDO)
        tb.AddSimpleButton(self.IDS.UNDO, 'Undo', icon_undo,
                     'Undo task action.')
        self.Bind(self.ribbon_button_bar_event, self.on_undo, id=self.IDS.UNDO)

        icon_redo = wx.ArtProvider.GetBitmap(wx.ART_REDO)
        tb.AddSimpleButton(self.IDS.REDO, 'Redo', icon_redo,
                     'Redo previous undo action.')
        self.Bind(self.ribbon_button_bar_event, self.on_redo, id=self.IDS.REDO)

        panel.SetSizer(sizer)
        tb.Realize()

    def is_initialized(self):
        if self.project is None:
            return False
        return True

    def on_undo(self, event):
        if not self.is_initialized():
            return
        self.command_processor.Undo()

    def on_redo(self, event):
        if not self.is_initialized():
            return
        self.command_processor.Redo()

    def get_stock_bitmap(self, art_id, size):
        return wx.ArtProvider.GetBitmap(art_id, size=size)

    def set_button_cursors(self):
        for button in self.ribbon_buttons:
            button.SetCursor(wx.Cursor(wx.CURSOR_HAND))

    def on_task_move_down(self, event):
        if self.project is None:
            return

        if self.project.selected_task_index is None:
            wx.MessageBox('A task shall be selected from the WBS before moving.', 'No Task Selected',
                          style=wx.OK_DEFAULT)
        else:
            index = self.project.selected_task_index

            if index == len(self.project.tasks) - 1:
                pass
            else:
                command = MoveTaskDownCommand(True, 'Move Task Down',
                                              self.project.selected_task_index,
                                              self.project)
                self.command_processor.Submit(command)

    def on_task_move_up(self, event):
        if self.project is None:
            return

        if self.project.selected_task_index is None:
            wx.MessageBox('A task shall be selected from the WBS before moving.', 'No Task Selected',
                          style=wx.OK_DEFAULT)
        else:
            index = self.project.selected_task_index

            if index == 0:
                pass
            else:
                command = MoveTaskUpCommand(True, 'Move Task Up',
                                            self.project.selected_task_index,
                                            self.project)
                self.command_processor.Submit(command)

    def on_new_project(self, event):
        dlg = wx.MessageDialog(self, 'Create new project?',
                               'New Project', wx.YES_NO | wx.CANCEL)

        # Ask for confirmation first before creating an empty file.
        if dlg.ShowModal() == wx.ID_YES:

            project_dict = {'tasks': []}

            with wx.FileDialog(self.parent, 'New project.', '', 'New Project',
                               wildcard='EasyPlan files (*.epn)|*.epn',
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return

                # Save the current content of the file
                pathname = file_dialog.GetPath()

                try:
                    with open(pathname, 'wb') as file:
                        pickle.dump(project_dict, file, pickle.DEFAULT_PROTOCOL)

                        self.initialize_project(project_dict)

                        self.parent.status_bar.SetStatusText(STATUS_PROJECT_CREATED)
                        self.parent.status_bar.SetStatusText(pathname, 1)
                    self.parent.project_file = pathname
                except IOError:
                    wx.LogError('Cannot save current file')

    def on_open_project(self, event):
        with wx.FileDialog(self.parent, 'Open project.', '',
                           wildcard='EasyPlan files (*.epn)|*.epn',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            # Save the current content of the file
            pathname = file_dialog.GetPath()
            try:
                with open(pathname, 'rb') as inp:
                    project_dict = pickle.load(inp)

                    self.parent.project_file = pathname

                    self.initialize_project(project_dict)
                    self.parent.status_bar.SetStatusText(STATUS_PROJECT_OPENED)
                    self.parent.status_bar.SetStatusText(pathname, 1)
            except IOError:
                wx.LogError('Cannot open current file')

    def initialize_project(self, project_dict):
        # Create new instance of project
        # 05/31/1988
        project = Project()
        if 'project_name' in project_dict:
            project.project_name = project_dict['project_name']
        project.tasks = project_dict['tasks']

        if 'interval_major_grid' in project_dict:
            project.interval_major_axis = project_dict['interval_major_grid']

        if 'start_date' in project_dict:
            sd = project_dict['start_date']
            start_date = wx.DateTime(sd[0], sd[1], sd[2])
            project.start_date = start_date
        else:
            project.start_date = wx.DateTime().Now()

        if 'project_name' in project_dict:
            project.project_name = project_dict['project_name']

        if 'project_manager' in project_dict:
            project.project_manager = project_dict['project_manager']

        self.parent.project = project

        self.project = project

        self.parent.left_pane.project = project
        self.parent.right_pane.project = project

        self.parent.left_pane.populate()
        self.parent.right_pane.redraw()

    def on_save_project(self, event):
        # Convert the date time to tuple
        sd: wx.DateTime = self.project.start_date
        day = sd.GetDay()
        month = sd.GetMonth()
        year = sd.GetYear()

        start_date = day, month, year

        p = {'path': self.parent.project_file,
             'tasks': self.project.tasks,
             'interval_major_grid': self.project.interval_major_axis,
             'start_date': start_date,
             'project_name': self.project.project_name,
             'project_manager': self.project.project_manager}

        if self.parent.project_file != '':
            path = self.parent.project_file
            try:
                with open(path, 'wb') as file:
                    pickle.dump(p, file, protocol=pickle.DEFAULT_PROTOCOL)
                    self.parent.status_bar.SetStatusText(STATUS_PROJECT_SAVED + ' : ' + path)
            except IOError:
                wx.LogError('Cannot save current file')

    def on_save_project_as(self, event):
        print('Save project as')

    def on_add_task(self, event):
        if self.project is None:
            return
        task = Task(project=self.project)

        selected_index = self.project.selected_task_index

        command = AddTaskCommand(True, 'Add Task', task, selected_index, self.project)

        self.command_processor.Submit(command)

    def on_delete_task(self, event):
        """
        Delete a given task from the selected row.
        :param event: A toolbar click event.
        :return:
        """
        if self.project is None:
            return

        successors = []
        for task in self.project.tasks:
            for predecessor in task.predecessors:
                if predecessor == self.project.tasks[self.project.selected_task_index]:
                    successors.append(task)

        if self.project.selected_task_index is None:
            wx.MessageBox('A task shall be selected from the WBS before deleting.', 'No Task Selected',
                          style=wx.OK_DEFAULT)
        else:
            # Ask user for confirmation
            index = self.project.selected_task_index

            if index <= len(self.project.tasks) - 1:
                dlg = wx.MessageBox('Delete the selected task?', 'Delete Task', style=wx.YES_NO | wx.CANCEL)
                if dlg == wx.YES:
                    command = RemoveTaskCommand(True, 'Delete Task',
                                                self.project.tasks[self.project.selected_task_index],
                                                self.project.selected_task_index,
                                                self.project,
                                                successors)

                    self.command_processor.Submit(command)

    def on_outdent_task(self, event):
        print('Outdent Task')

    def on_indent_task(self, event):
        print('Indent task')

    def on_split_task(self, event):
        if self.project is None:
            return

        if self.project.selected_task_segment is not None:
            dlg = SplitTaskDialog(self.parent)
            res = dlg.ShowModal()
            if res == ID_OK:
                dlg.Destroy()
        else:
            wx.MessageBox('A task segment must be selected before splitting.')

    def on_merge_segments(self, event):
        if self.project is None:
            return

        if self.project.selected_task_index is None:
            return
        task = self.project.selected_task
        command = MergeTaskSegments(True, 'Merge Task Segments',
                                    task)
        self.command_processor.Submit(command)

    def on_rename(self, event):
        print(self.project.selected_task_index)

    def on_move_segment(self, event):
        if self.project is None:
            return

        if self.project.selected_task_segment is not None:
            # Open dialog
            dlg = MoveTaskSegmentDialog(self.parent)
            res = dlg.ShowModal()
            if res == ID_OK:
                dlg.Destroy()
        else:
            wx.MessageBox('A task segment must be selected first.',
                          'Error',
                          wx.OK | wx.ICON_ERROR)

    def on_project_information_clicked(self, event):
        if self.project is None:
            return
        dlg = ProjectInformationDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            project_name = dlg.notebook.entry_project_title.GetValue()
            project_manager = dlg.notebook.entry_project_manager.GetValue()
            start_date = dlg.notebook.entry_start_date.GetValue()

            self.project.project_name = project_name
            self.project.project_manager = project_manager
            self.project.start_date = start_date

            # Update status message
            self.parent.status_bar.SetStatusText('Project information updated.')

            dlg.Destroy()

