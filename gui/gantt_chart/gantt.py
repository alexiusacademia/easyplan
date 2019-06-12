import wx

from .bar import Bar


class GanttChart(wx.Window):
    wbs = None
    project = None
    header_height = 0

    BAR_SCALE = 10

    bars = []

    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)

        self.wbs = wbs
        self.project = project

        self.SetBackgroundColour((255, 255, 255))
        self.Bind(wx.EVT_PAINT, self.redraw)

    def redraw(self, event):
        """
        Handles the drawing functionalizties of the gantt chart canvas.
        :param event:
        :return:
        """
        self.header_height = self.wbs.GetGridColLabelWindow().Size[1]
        num_rows = self.wbs.GetNumberRows()
        if num_rows > 0:
            row_height = self.wbs.GetRowSize(0)
            self.draw_hor_grids(self.GetSize()[0], num_rows, row_height)
            self.draw_task_bars()
        else:
            row_height = 0

    def trigger_draw(self):
        """
        Refresh the window content.
        :return:
        """
        self.Refresh()
        self.draw_task_bars()

    def draw_hor_grids(self, length, num, vert_distance):
        """
        Draw the horizontal grid lines based on the number of rows
        of tasks.
        :param length: The width of thee gantt chart canvas.
        :param num: Number of tasks
        :param vert_distance: The distance between grid line (Matched to the height of table row.)
        """
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.LIGHT_GREY, 1))

        for i in range(num + 1):
            y = i * vert_distance + self.header_height
            dc.DrawLine(0, y, length, y)

    def draw_task_bars(self):
        for b in self.bars:
            if isinstance(b, Bar):
                b.Destroy()
        self.bars.clear()

        tasks = self.project.tasks
        if len(tasks) > 0:
            index = 0
            for task in tasks:
                bar = Bar(self,
                          task,
                          index * self.wbs.GetRowSize(0) + self.header_height,
                          self.BAR_SCALE)
                self.bars.append(bar)
                index += 1
