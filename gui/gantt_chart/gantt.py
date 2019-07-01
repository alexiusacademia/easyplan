import wx
from pubsub import pub

from .bar import BarSegment
from constants import *


class GanttChart(wx.ScrolledCanvas):
    wbs = None
    project = None

    bars = []

    parent = None

    def __init__(self, parent, project, wbs):
        wx.Window.__init__(self, parent)

        self.wbs = wbs
        self.project = project
        self.parent = parent.GetParent()

        self.SetBackgroundColour((255, 255, 255))

        self.Bind(wx.EVT_PAINT, self.on_paint)

        pub.subscribe(self.on_project_updated, EVENT_PROJECT_UPDATED)
        pub.subscribe(self.on_task_start_updated, EVENT_TASK_START_UPDATED)
        pub.subscribe(self.redraw, EVENT_TASK_DURATION_UPDATED)
        pub.subscribe(self.redraw, EVENT_TASK_PREDECESSORS_UPDATED)

        # self.SetScrollbars(1, 1, 1000, 1000, 0, 0)

    def on_paint(self, event):
        if self.project is not None:
            self.ClearBackground()
            self.draw_hor_grids(self.GetSize()[0], len(self.project.tasks), WBS_ROW_HEIGHT)
            self.draw_vertical_major_grid_lines()
            self.draw_predecessor_lines()

    def redraw(self):
        """
        Handles the drawing functions of the gantt chart canvas.
        :param event:
        :return:
        """
        self.draw_task_bars()
        self.draw_predecessor_lines()

    def on_task_start_updated(self, index, start):
        y = index * WBS_ROW_HEIGHT + WBS_HEADER_HEIGHT
        for bar in self.bars:
            if bar.GetPosition()[1] == y:
                bar_x = bar.GetPosition()[0]
                bar.SetPosition((start * BAR_SCALE - bar_x), y)
        self.redraw()

    def draw_predecessor_lines(self):
        dc = wx.ClientDC(self)
        pen = wx.Pen(wx.RED, 2)
        dc.SetPen(pen)

        tasks = self.project.tasks
        for index, task in enumerate(tasks):
            # Get the predecessors of the task
            if len(task.predecessors) > 0:
                # Get the task start coordinate
                task_x = task.start_day * BAR_SCALE
                task_y = WBS_HEADER_HEIGHT + (index * WBS_ROW_HEIGHT) + WBS_ROW_HEIGHT / 2

                for p in task.predecessors:
                    p_end = p.start_day + p.get_virtual_duration()
                    p_x = p_end * BAR_SCALE
                    p_index = tasks.index(p)
                    p_y = WBS_HEADER_HEIGHT + (p_index * WBS_ROW_HEIGHT) + WBS_ROW_HEIGHT/2

                    mid_x = (task_x + p_x) / 2

                    points = [(task_x, task_y), (mid_x, task_y), (mid_x, p_y), (p_x, p_y)]
                    dc.DrawLines(points)

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
                                 ts.start * BAR_SCALE,
                                 index * WBS_ROW_HEIGHT + WBS_HEADER_HEIGHT,
                                 ts.duration * BAR_SCALE,
                                 BAR_HEIGHT,
                                 task,
                                 ts)

                self.bars.append(bar)

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

    def draw_vertical_major_grid_lines(self):
        major_interval = self.project.interval_major_axis
        gantt_width, gantt_height = self.GetSize()
        number_of_lines = int(gantt_width / BAR_SCALE / major_interval)

        dc = wx.ClientDC(self)
        pen = wx.Pen(wx.LIGHT_GREY, 1)
        dc.SetPen(pen)

        for i in range(number_of_lines):
            dc.DrawLine(i * major_interval * BAR_SCALE, 0,
                        i * major_interval * BAR_SCALE, gantt_height)

    def on_project_updated(self):
        self.redraw()
