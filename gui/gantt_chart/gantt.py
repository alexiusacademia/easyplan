import wx

from .bar import BarSegment
from .constants import *


class GanttChart(wx.Window):
    wbs = None
    project = None

    BAR_SCALE = 10
    BAR_THICKNESS = 20

    bars = []

    parent = None

    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)

        self.wbs = wbs
        self.project = project
        self.parent = parent.GetParent()

        self.SetBackgroundColour((255, 255, 255))

        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        self.ClearBackground()
        self.draw_hor_grids(self.GetSize()[0], len(self.project.tasks), WBS_ROW_HEIGHT)
        self.draw_predecessor_lines()

    def redraw(self):
        """
        Handles the drawing functions of the gantt chart canvas.
        :param event:
        :return:
        """
        self.draw_task_bars()

    def draw_predecessor_lines(self):
        dc = wx.ClientDC(self)

        tasks = self.project.tasks
        for index, task in enumerate(tasks):
            # Get the predecessor of the task
            if task.predecessor != '':
                # Now get the predecessor of the task
                predecessor = self.project.tasks[int(task.predecessor)]

                # Now get the start and virtual duration of it
                predecessor_start = predecessor.start_day
                predecessor_duration = predecessor.get_virtual_duration()

                # This end property is the earliest possible that the successor task
                # can start but the actual end is the day before it.
                # For example: If a task starts at day 1 and has a duration of 1 day,
                # It ends on day 1 also, but the earliest possible that the next task can
                # start is the day 2.
                predecessor_end = predecessor_start + predecessor_duration

                # Convert the predecessor end to coordinate
                pred_index = int(task.predecessor)
                pred_y = WBS_ROW_HEIGHT * pred_index + WBS_ROW_HEIGHT/2 + WBS_HEADER_HEIGHT
                pred_x = BAR_SCALE * (predecessor_end - 1)

                # Now get the coordinate of the start of the task
                task_y = WBS_ROW_HEIGHT * index + WBS_ROW_HEIGHT/2 + WBS_HEADER_HEIGHT
                task_x = (task.start_day - 1) * BAR_SCALE

                # Get the middle of between these two task bars
                m_x = abs(pred_x - task_x) / 2 + min(pred_x, task_x)

                pen = wx.Pen(wx.RED, 2)
                dc.SetPen(pen)
                # dc.DrawLine(pred_x, pred_y, task_x, task_y)
                dc.DrawLines([(pred_x, pred_y),
                              (m_x, pred_y),
                              (m_x, task_y),
                              (task_x, task_y)])

    def draw_hor_grids(self, length, num, vert_distance):
        """
        Draw the horizontal grid lines based on the number of rows
        of tasks.
        :param length: The width of thee gantt chart canvas.
        :param num: Number of tasks
        :param vert_distance: The distance between grid line (Matched to the height of table row.)
        """
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0.75))

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
                # bar.Bind(wx.EVT_LEFT_DCLICK, lambda event, t=task, ts=ts: self.on_double_clicked(event, t, ts))

                self.bars.append(bar)
                # print(ts.start, ' - ', ts.duration, end=', ')
            # print('\n= = = = =')

    def on_double_clicked(self, event, task, task_segment):
        if isinstance(event, wx.MouseEvent):
            loc = event.GetPosition()
            x = loc[0]
            day = int(x / BAR_SCALE) + 1
            result = task.split_task(task_segment, day)
            ts1, ts2 = result[1]
            print('ts1:', ts1.start, ts1.duration)
            print('ts2', ts2.start, ts2.duration)
            bs = event.GetEventObject()

            x, y = bs.GetPosition()

            # Delete and hide the source bar segment
            # self.bars.remove(bs)
            bs.Hide()

            for ts in result[1]:
                bs1 = BarSegment(self,
                                 ts.start * BAR_SCALE,
                                 y,
                                 ts.duration * BAR_SCALE,
                                 BAR_HEIGHT, task, ts)
                self.bars.append(bs1)
