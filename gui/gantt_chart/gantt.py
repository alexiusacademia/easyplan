import wx


class GanttChart(wx.Window):
    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)
        self.SetBackgroundColour((255, 255, 255))