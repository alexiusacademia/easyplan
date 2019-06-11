# Import built-in modules
import wx
import wx.lib.mixins.listctrl as listmix

# Import project modules
from core.task import Task
from core.project import Project


class WorkBreakdownStructure(wx.ListCtrl, listmix.TextEditMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)
        listmix.TextEditMixin.__init__(self)
        # listmix.ListCtrlAutoWidthMixin.__init__(self)


class TaskListPane(wx.Panel):
    def __init__(self, parent, project):
        wx.Panel.__init__(self, parent=parent, style=wx.WANTS_CHARS)

        self.project = project
        self.parent = parent
        sizer = wx.GridBagSizer(vgap=5, hgap=5)

        self.task_list_ctrl = WorkBreakdownStructure(
            self,
            style=wx.LC_REPORT |
                  wx.BORDER_NONE |
                  # wx.BORDER_SUNKEN |
                  wx.LC_SINGLE_SEL |
                  wx.LC_HRULES |
                  wx.LC_VRULES
        )
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.task_list_ctrl)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.on_end_editing, self.task_list_ctrl)

        # Create the default columns
        self.task_list_ctrl.InsertColumn(0, 'Id')
        self.task_list_ctrl.InsertColumn(1, 'Task Name', width=200)
        self.task_list_ctrl.InsertColumn(2, 'Start', width=60, format=wx.LIST_FORMAT_CENTRE)
        self.task_list_ctrl.InsertColumn(3, 'Duration', width=60, format=wx.LIST_FORMAT_CENTRE)
        self.task_list_ctrl.InsertColumn(4, 'Predecessor', width=80, format=wx.LIST_FORMAT_CENTER)

        self.set_column_sizes()

        sizer.Add(self.task_list_ctrl, pos=(0, 0),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)

    def on_item_selected(self, evt):
        selected_index = self.task_list_ctrl.GetFocusedItem()
        self.project.selected_task_index = selected_index

    def on_end_editing(self, event):
        """
        Update the task object after editing some properties.
        :param event: Event fired after ENTER is pressed or cell has lost its focus.
        :return:
        """
        index = event.GetIndex()
        col = event.GetColumn()
        value = event.GetLabel()
        task = self.project.tasks[index]
        if col == 1:
            task.task_name = value
        elif col == 2:
            task.start_day = int(value)
        elif col == 3:
            task.set_duration(int(value))
        elif col == 4:
            task.predecessor = int(value)

    def redraw_project(self):
        # First clear content
        li = self.task_list_ctrl
        li.ClearAll()

        li.InsertColumn(0, 'Id')
        li.InsertColumn(1, 'Task Name', width=200)
        li.InsertColumn(2, 'Start', width=60, format=wx.LIST_FORMAT_CENTRE)
        li.InsertColumn(3, 'Duration', width=60, format=wx.LIST_FORMAT_CENTRE)
        li.InsertColumn(4, 'Predecessor', width=80, format=wx.LIST_FORMAT_CENTER)

        self.set_column_sizes()

        index = 0
        for task in self.project.tasks:
            li.InsertItem(index, str(index))
            li.SetItem(index, 1, task.task_name)
            li.SetItem(index, 2, str(task.start_day))
            li.SetItem(index, 3, str(task.get_duration()))
            if task.predecessor is not None:
                li.SetItem(index, 4, str(task.predecessor))

            index += 1

    def set_column_sizes(self):
        self.task_list_ctrl.SetColumnWidth(0, 30)
        self.task_list_ctrl.SetColumnWidth(1, 200)
        self.task_list_ctrl.SetColumnWidth(2, 50)
        self.task_list_ctrl.SetColumnWidth(3, 50)
        self.task_list_ctrl.SetColumnWidth(4, 50)
        self.task_list_ctrl.SetColumnWidth(5, 50)

# TODO Create dialog for renaming task
# TODO Create dialog for splitting
# TODO Add confirmation on task deletion.
# TODO Add dialog for adding task.
# TODO Update the project object after cell editing.
