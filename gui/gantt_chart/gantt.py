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
        header_height = self.wbs.GetGridColLabelWindow().Size[1]
        num_rows = self.wbs.GetNumberRows()
        if num_rows > 0:
            row_height = self.wbs.GetRowSize(0)
        else:
            row_height = 0
        print(row_height)

    def trigger_draw(self):
        self.Refresh()

