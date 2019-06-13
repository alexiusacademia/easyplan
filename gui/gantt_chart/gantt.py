import wx

from .bar import Bar, BarSegment


class GanttChart(wx.Window):
    wbs = None
    project = None
    header_height = 0

    BAR_SCALE = 10
    BAR_THICKNESS = 20

    bars = []

    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)

        self.wbs = wbs
        self.project = project

        self.SetBackgroundColour((255, 255, 255))
        self.redraw()

    # def redraw(self, event):
    def redraw(self):
        print('Redraw')
        """
        Handles the drawing functionalities of the gantt chart canvas.
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
        self.delete_bars()
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

    def delete_bars(self):
        for b in self.bars:
            if isinstance(b, BarSegment):
                b.Destroy()
        self.bars.clear()

    def draw_task_bars(self):
        row_size = self.wbs.GetRowSize(0)

        tasks = self.project.tasks
        if len(tasks) > 0:
            index = 0
            for task in tasks:
                '''
                bar = Bar(self,
                          task,
                          index * row_size + self.header_height,
                          self.BAR_SCALE)
                          '''
                for ts in task.task_segments:
                    bar = BarSegment(self,
                                     (ts.start - 1) * self.BAR_SCALE,
                                     index * row_size + self.header_height,
                                      ts.duration * self.BAR_SCALE,
                                     self.BAR_THICKNESS)
                    self.bars.append(bar)
                index += 1
