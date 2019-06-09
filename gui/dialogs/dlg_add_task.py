import wx


class AddTaskDialog(wx.Dialog):
    def __init__(self):
        super().__init__(parent=None, title='Add Task')
        self.panel = wx.Panel(parent=self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        label_task_name = wx.StaticText(self.panel, label='Task Name', size=(100, -1))
        # self.sizer.Add(label_task_name, pos=(0, 0))

        entry_task_name = wx.TextCtrl(self.panel)
        # self.sizer.Add(entry_task_name, pos=(0, 1), flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        box_task_name = wx.BoxSizer(wx.HORIZONTAL)
        self.add_padding(box_task_name, 5)
        box_task_name.Add(label_task_name, 1)
        box_task_name.Add(entry_task_name, 2)
        self.add_padding(box_task_name, 5)

        label_task_start = wx.StaticText(self.panel, label='Start', size=(100, -1))
        # self.sizer.Add(label_task_start, pos=(1, 0))

        entry_task_start = wx.TextCtrl(self.panel)
        # self.sizer.Add(entry_task_start, pos=(1, 1))
        box_task_start = wx.BoxSizer(wx.HORIZONTAL)
        self.add_padding(box_task_start, 5)
        box_task_start.Add(label_task_start, 1)
        box_task_start.Add(entry_task_start, 0)
        self.add_padding(box_task_start, 5)

        label_task_duration = wx.StaticText(self.panel, label='Duration', size=(100, -1))
        # self.sizer.Add(label_task_duration, pos=(2, 0))

        entry_task_duration = wx.TextCtrl(self.panel)
        # self.sizer.Add(entry_task_duration, pos=(2, 1))
        box_task_duration = wx.BoxSizer(wx.HORIZONTAL)
        self.add_padding(box_task_duration, 5)
        box_task_duration.Add(label_task_duration, 1)
        box_task_duration.Add(entry_task_duration, 0)
        self.add_padding(box_task_duration, 5)

        # self.sizer.AddGrowableCol(1)
        self.add_padding(self.sizer, 5)
        self.sizer.Add(box_task_name, 0, flag=wx.EXPAND)
        self.add_padding(self.sizer, 5)
        self.sizer.Add(box_task_start, 0, wx.EXPAND)
        self.add_padding(self.sizer, 5)
        self.sizer.Add(box_task_duration, 0, wx.EXPAND)

        self.panel.SetSizer(self.sizer)

    def add_padding(self, sizer, size):
        sizer.AddSpacer(size)