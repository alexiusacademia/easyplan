# Import built-in modules
import wx
import wx.ribbon
import os

# Import project modules
from .dialogs.dlg_add_task import AddTaskDialog
from .dialogs.dlg_split_task import SplitTaskDialog
from core.task import Task
from .gantt_chart.constants import *


class Ribbon(wx.ribbon.RibbonBar):
    ribbon_buttons = []
    project = None
    task_index = None

    class IDS:
        # -----------
        ADD_TASK = 10
        DELETE_TASK = 20
        INDENT_TASK = 30
        OUTDENT_TASK = 40
        # -----------
        SPLIT_TASK = 50
        RENAME_TASK = 60

    RIBBON_BUTTON_SIZE = (22, 22)

    def __init__(self, parent, project, wbs):
        super().__init__(parent=parent)
        self.create_pages()
        self.set_button_cursors()

        self.parent = parent

        self.project = project

        self.wbs = wbs

    def create_pages(self):
        self.page_gantt_chart()
        self.page_scurve()
        self.Realize()

    # --------------
    # Pages
    # --------------
    def page_gantt_chart(self):
        # ---------------- GANTT CHART PAGE ---------------- #
        gantt_page = wx.ribbon.RibbonPage(self, label='Gantt Chart')
        self.panel_gantt_basic(gantt_page)
        self.panel_gantt_edit(gantt_page)

    def page_scurve(self):
        # ---------------- GANTT CHART PAGE ---------------- #

        scurve_page = wx.ribbon.RibbonPage(self, label='S-Curve')

        scurve_panel = wx.Panel(parent=scurve_page)
        scurve_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        btn1 = wx.Button(parent=scurve_panel, label='SCurve Button')
        scurve_page_sizer.Add(btn1, pos=(0, 0))

        scurve_panel.SetSizer(scurve_page_sizer)

    # --------------
    # Ribbon Panels
    # --------------
    def panel_gantt_basic(self, page):
        # -- Task Panel -- #
        gantt_task_panel = wx.ribbon.RibbonPanel(parent=page, label='BASIC',
                                                 style=wx.ribbon.RIBBON_PANEL_DEFAULT_STYLE)

        gantt_page_sizer = wx.BoxSizer(wx.VERTICAL)

        tb = wx.ToolBar(gantt_task_panel, style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.NO_BORDER | wx.TB_DOCKABLE)
        tb.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        gantt_page_sizer.Add(tb, 0, wx.EXPAND)

        # Add task button
        icon_add_task = wx.ArtProvider.GetBitmap(wx.ART_PLUS, size=self.RIBBON_BUTTON_SIZE)
        tb.AddTool(self.IDS.ADD_TASK, 'Add New Task', icon_add_task, 'Add new task to the project.', wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.on_add_task, id=self.IDS.ADD_TASK)

        # Delete task button
        icon_delete_task = self.get_stock_bitmap(wx.ART_MINUS, size=self.RIBBON_BUTTON_SIZE)
        tb.AddTool(self.IDS.DELETE_TASK, 'Delete Task', icon_delete_task, 'Remove the selected task from project.',
                   wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.on_delete_task, id=self.IDS.DELETE_TASK)

        tb.AddSeparator()

        # Outdent task button
        icon_outdent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, size=self.RIBBON_BUTTON_SIZE)
        tb.AddTool(self.IDS.OUTDENT_TASK, 'Outdent Task', icon_outdent_task,
                   'Remove the task from the immediate parent.', wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.on_outdent_task, id=self.IDS.OUTDENT_TASK)

        # Indent task button
        icon_indent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, size=self.RIBBON_BUTTON_SIZE)
        tb.AddTool(self.IDS.INDENT_TASK, 'Indent Task', icon_indent_task, 'Set the above task as parent.',
                   wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.on_indent_task, id=self.IDS.INDENT_TASK)

        tb.Realize()

        gantt_task_panel.SetSizer(gantt_page_sizer)
        # -- End Task Panel -- #

    def panel_gantt_edit(self, page):
        panel = wx.ribbon.RibbonPanel(parent=page, label='EDIT',
                                      style=wx.ribbon.RIBBON_PANEL_DEFAULT_STYLE)

        tb = wx.ToolBar(panel, style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.NO_BORDER | wx.TB_DOCKABLE)
        tb.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tb, 0, wx.EXPAND)

        icon_split = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                             'ribbon', 'gantt', 'split.png'))
        tb.AddTool(self.IDS.SPLIT_TASK, 'Split Task', icon_split, 'Split a task segment.', wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.on_split_task, id=self.IDS.SPLIT_TASK)

        icon_rename = wx.Bitmap(os.path.join(os.getcwd(), 'gui', 'assets', 'icons',
                                             'ribbon', 'gantt', 'rename.png'))
        tb.AddTool(self.IDS.RENAME_TASK, 'Rename Task', icon_rename,
                   'Rename task.', wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.on_rename, id=self.IDS.RENAME_TASK)

        panel.SetSizer(sizer)
        tb.Realize()

    def get_stock_bitmap(self, art_id, size):
        return wx.ArtProvider.GetBitmap(art_id, size=size)

    def set_button_cursors(self):
        for button in self.ribbon_buttons:
            button.SetCursor(wx.Cursor(wx.CURSOR_HAND))

    def on_add_task(self, event):
        if self.project.selected_task_index is not None:
            index = self.project.selected_task_index
            self.project.tasks.insert(index, Task())
        else:
            self.project.add_task(Task())
        # self.parent.refresh(populate=True)
        self.project.selected_task_index = None
        self.wbs.populate()
        self.parent.right_pane.redraw()

    def on_delete_task(self, event):
        """
        Delete a given task from the selected row.
        :param event: A toolbar click event.
        :return:
        """
        if self.project.selected_task_index is None:
            wx.MessageBox('A task shall be selected from the WBS before deleting.', 'Delete Task',
                          style=wx.OK_DEFAULT)
        else:
            # Ask user for confirmation
            # TODO Do some necessary checking before deleting. This can also be implemented on the core API.
            index = self.project.selected_task_index

            if index <= len(self.project.tasks) - 1:
                dlg = wx.MessageBox('Delete the selected task?', 'Delete Task', style=wx.YES_NO | wx.CANCEL)
                if dlg == wx.YES:
                    self.project.remove_task(self.project.tasks[index])
                    self.parent.left_pane.populate()
                    self.parent.right_pane.redraw()
                    self.project.selected_task_index = None

    def on_outdent_task(self, event):
        print('Outdent Task')

    def on_indent_task(self, event):
        print('Indent task')

    def on_split_task(self, event):
        dlg = SplitTaskDialog(self.parent)
        if self.project.selected_task_segment is not None:

            res = dlg.ShowModal()
            if res == ID_OK:
                dlg.Destroy()
        else:
            wx.MessageBox('A task segment must be selected before splitting.')

    def on_rename(self, event):
        print(self.project.selected_task_index)
