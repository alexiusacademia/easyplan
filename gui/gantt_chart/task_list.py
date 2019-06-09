import wx

# Import project modules
from core.task import Task
from core.project import Project


class TaskListPane(wx.Panel):
    def __init__(self, parent, project):
        wx.Panel.__init__(self, parent=parent)

        sizer = wx.GridBagSizer(vgap=5, hgap=5)

        self.task_list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL | wx.LC_EDIT_LABELS | wx.LC_HRULES | wx.LC_VRULES
        )
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.task_list_ctrl)

        # Create the default columns
        self.task_list_ctrl.InsertColumn(0, 'Task', width=200)
        self.task_list_ctrl.InsertColumn(1, 'Start', width=60, format=wx.LIST_FORMAT_CENTRE)
        self.task_list_ctrl.InsertColumn(2, 'Duration', width=60, format=wx.LIST_FORMAT_CENTRE)

        # self.task_list_ctrl.InsertItem(0, 'Untitled Task')
        # self.task_list_ctrl.SetItem(0, 1, str(0))
        # self.task_list_ctrl.SetItem(0, 2, str(1))

        sizer.Add(self.task_list_ctrl, pos=(0, 0),
                  flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)

    def on_item_selected(self, evt):
        print(evt.GetText())

    def add_task(self, task_object, *args):
        """
        Add a task to the specific row.
        :param task_object:
        :param row_index:
        :return:
        """
        if len(args) > 0:
            # The index is given so we insert the task on that index
            index = args[0]

