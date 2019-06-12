import wx


class GanttChart(wx.Window):
    wbs = None
    project = None

    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)

        self.wbs = wbs
        self.project = project

        self.SetBackgroundColour((255, 255, 255))
        self.Bind(wx.EVT_PAINT, self.redraw)

    def redraw(self, event):
        print(self.wbs.GetNumberRows())

    def trigger_draw(self):
        self.Refresh()
