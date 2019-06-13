import wx

from .bar import Bar, BarSegment
from .constants import *


class GanttChart(wx.Window):
    wbs = None
    project = None

    BAR_SCALE = 10
    BAR_THICKNESS = 20

    bars = []

    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)

        self.wbs = wbs
        self.project = project

        self.SetBackgroundColour((255, 255, 255))
        # self.redraw()

    # def redraw(self, event):
    def redraw(self):
        """
        Handles the drawing functionalities of the gantt chart canvas.
        :param event:
        :return:
        """
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
            y = i * vert_distance + WBS_HEADER_HEIGHT
            dc.DrawLine(0, y, length, y)

    def delete_bars(self):
        for b in self.bars:
            if isinstance(b, BarSegment):
                b.Destroy()
        self.bars.clear()

    def draw_task_bars(self):
        self.delete_bars()

        tasks = self.project.tasks

        for index, task in enumerate(tasks):
            for ts in task.task_segments:
                bar = BarSegment(self,
                                 (ts.start - 1) * self.BAR_SCALE,
                                 index * WBS_ROW_HEIGHT + WBS_HEADER_HEIGHT,
                                 ts.duration * self.BAR_SCALE,
                                 self.BAR_THICKNESS)

                self.bars.append(bar)
        print(self.bars)
