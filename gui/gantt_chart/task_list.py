import wx


class TaskListPane(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        sizer = wx.GridBagSizer(vgap=5, hgap=5)

        self.task_list_ctrl = wx.ListCtrl(
            self,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        # Create the default columns
        self.task_list_ctrl.InsertColumn(0, 'Task', width=200)
        self.task_list_ctrl.InsertColumn(1, 'Start', width=140)
        self.task_list_ctrl.InsertColumn(2, 'Duration', width=140)

        sizer.Add(self.task_list_ctrl, pos=(0, 0),
                  flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM)

        sizer.AddGrowableRow(0)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)
