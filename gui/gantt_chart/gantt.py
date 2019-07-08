import wx
from wx.lib.scrolledpanel import ScrolledPanel
from pubsub import pub

from .bar import BarSegment
from constants import *


class GanttChart(ScrolledPanel):
    wbs = None
    project = None

    bars = []

    parent = None

    chart_width = 0
    number_major_vertical_grid = 0

    timeline_dates = []

    def __init__(self, parent, project, wbs):
        # wx.Window.__init__(self, parent)
        ScrolledPanel.__init__(self, parent)

        self.wbs = wbs
        self.project = project
        self.parent = parent.GetParent()

        self.SetBackgroundColour((255, 255, 255))

        self.Bind(wx.EVT_PAINT, self.on_paint)

        pub.subscribe(self.on_project_updated, EVENT_PROJECT_UPDATED)
        pub.subscribe(self.on_task_start_updated, EVENT_TASK_START_UPDATED)
        pub.subscribe(self.redraw, EVENT_TASK_DURATION_UPDATED)
        pub.subscribe(self.redraw, EVENT_TASK_PREDECESSORS_UPDATED)
        pub.subscribe(self.redraw, EVENT_PROJECT_OPENED)

        self.SetupScrolling(scrollIntoView=False)
        # self.SetScrollbars(1, 1, 1000, 1000, 0, 0)

    def on_paint(self, event):
        if self.project is not None:
            self.ClearBackground()
            self.draw_hor_grids(self.GetSize()[0], len(self.project.tasks), WBS_ROW_HEIGHT)
            self.draw_vertical_major_grid_lines()
            self.draw_predecessor_lines()
            # self.draw_timeline()

    def redraw(self):
        """
        Handles the drawing functions of the gantt chart canvas.
        :param event:
        :return:
        """
        self.draw_task_bars()
        self.draw_predecessor_lines()
        self.draw_timeline()
        canvas_width, canvas_height = self.GetSize()
        gantt_width = self.project.get_project_duration() * BAR_SCALE
        gantt_height = WBS_HEADER_HEIGHT + len(self.project.tasks) * BAR_HEIGHT

        pixel_per_unit = 20
        no_units_x = int(gantt_width / pixel_per_unit)
        no_units_y = int(gantt_height / pixel_per_unit)
        '''
        self.SetScrollbars(pixel_per_unit,
                           pixel_per_unit,
                           no_units_x,
                           no_units_y)'''

    def on_task_start_updated(self, index, start):
        y = index * WBS_ROW_HEIGHT + WBS_HEADER_HEIGHT
        for bar in self.bars:
            if bar.GetPosition()[1] == y:
                bar_x = bar.GetPosition()[0]
                bar.SetPosition((start * BAR_SCALE - bar_x), y)
        self.redraw()

    def draw_predecessor_lines(self):
        dc = wx.ClientDC(self)
        pen = wx.Pen(wx.BLACK, 1)
        dc.SetPen(pen)

        tasks = self.project.tasks
        for index, task in enumerate(tasks):
            # Get the predecessors of the task
            if len(task.predecessors) > 0:
                # Get the task start coordinate
                task_x = (task.start_day - 1) * BAR_SCALE
                task_y = WBS_HEADER_HEIGHT + (index * WBS_ROW_HEIGHT) + WBS_ROW_HEIGHT / 2

                for p in task.predecessors:
                    p_end = p.start_day + p.get_virtual_duration()
                    p_x = (p_end - 1) * BAR_SCALE
                    p_index = tasks.index(p)
                    p_y = WBS_HEADER_HEIGHT + (p_index * WBS_ROW_HEIGHT) + WBS_ROW_HEIGHT / 2

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
                                 (ts.start - 1) * BAR_SCALE,
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

        self.number_major_vertical_grid = number_of_lines = int(gantt_width / BAR_SCALE / major_interval)

        self.chart_width = self.project.get_project_duration() * BAR_SCALE
        if self.chart_width > gantt_width:
            number_of_lines = int(self.chart_width / (BAR_SCALE * major_interval))

        dc = wx.ClientDC(self)
        pen = wx.Pen(wx.LIGHT_GREY, 1)
        dc.SetPen(pen)

        for i in range(number_of_lines):
            dc.DrawLine(i * major_interval * BAR_SCALE, 0,
                        i * major_interval * BAR_SCALE, gantt_height)

    def on_project_updated(self):
        self.redraw()

    def draw_timeline(self):
        for tld in self.timeline_dates:
            if isinstance(tld, wx.StaticText):
                tld.Destroy()
        self.timeline_dates.clear()

        span_week = wx.DateSpan(0, 0, 1)
        date_display: wx.DateTime = self.project.start_date

        y_pos = WBS_HEADER_HEIGHT - 20

        for i in range(self.number_major_vertical_grid):
            str_date = date_display.Format('%m/%d/%g')
            st = wx.StaticText(self, label=str_date, pos=((i * 7 * BAR_SCALE), y_pos))
            self.timeline_dates.append(st)
            date_display.Add(span_week)
