import wx

from .bar import BarSegment
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
        """
        Delete all bar segments created.
        :return:
        """
        for b in self.bars:
            if isinstance(b, BarSegment):
                b.Destroy()
        self.bars.clear()

    def draw_task_bars(self):
        """
        Draw each bar segment for each task.
        :return:
        """
        self.delete_bars()

        tasks = self.project.tasks

        for index, task in enumerate(tasks):
            for ts in task.task_segments:
                bar = BarSegment(self,
                                 (ts.start - 1) * self.BAR_SCALE,
                                 index * WBS_ROW_HEIGHT + WBS_HEADER_HEIGHT,
                                 ts.duration * self.BAR_SCALE,
                                 self.BAR_THICKNESS,
                                 task,
                                 ts)
                bar.Bind(wx.EVT_LEFT_DCLICK, lambda event, t=task, ts=ts: self.on_double_clicked(event, t, ts))

                self.bars.append(bar)
                print(ts.start, ' - ', ts.duration, end=', ')
            print('\n= = = = =')

    def on_double_clicked(self, event, task, task_segment):
        if isinstance(event, wx.MouseEvent):
            loc = event.GetPosition()
            x = loc[0]
            day = int(x / BAR_SCALE) + 1
            task.split_task(task_segment, day)

            false_bar = BarSegment(self,
                                   (day + 1) * BAR_SCALE,
                                   event.GetEventObject().GetPosition()[1],
                                   (task_segment.duration - day) * BAR_SCALE,
                                   BAR_HEIGHT, task, task_segment)
            bs = event.GetEventObject()
            bs.SetSize(day*BAR_SCALE, BAR_HEIGHT)