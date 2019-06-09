import wx


class AddTaskDialog(wx.Dialog):
    def __init__(self):
        self.panel = wx.Panel(parent=self)
        self.sizer = wx.GridBagSizer(vgap=5, hgap=5)
        self.panel.SetSizer(self.sizer)

        label_task_name = wx.StaticText(label='Task Name')
        self.sizer.Add(label_task_name, pos=(0, 0))

        entry_task_name = wx.TextEntry()
        self.sizer.Add(entry_task_name, pos=(0, 1))