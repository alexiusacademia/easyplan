import wx

from constants import *
from ..dialogs.dlg_split_task import SplitTaskDialog
from core.task_segment import TaskSegment
from core.project import Project

BG_RECEIVED_FOCUS = wx.Colour(0, 0, 0)
BG_DEFAULT = wx.Colour(0, 0, 255)


class BarSegment(wx.Panel):

    task_segment = None
    task = None
    parent = None
    project = None

    def __init__(self, parent, x, y, l, h, task, task_segment):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)

        self.task_segment: TaskSegment = task_segment
        self.task = task
        self.parent = parent
        self.project: Project = self.parent.project

        y_adjustment = (WBS_ROW_HEIGHT - BAR_HEIGHT) / 2

        self.SetPosition((x, y + y_adjustment))
        self.SetSize(l, h)
        self.SetBackgroundColour(BG_DEFAULT)

        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))

        # TRefresh s needed to work on Windows
        self.Refresh()

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
        self.Bind(wx.EVT_SET_FOCUS, self.on_received_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_lost_focus)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)

    def on_mouse_left_down(self, event):
        self.SetFocus()
        self.mouse_start_position = event.GetPosition().x

    def on_mouse_move(self, event):
        if not event.Dragging or not event.LeftIsDown():
            return

        # Get the bar's current position
        starting_point = self.GetPosition()[0]

        # Initial mouse position
        start_x = self.mouse_start_position

        dx = (event.GetPosition()[0] - start_x)

        new_x = starting_point + dx

        # Set the left limit
        left_limit = 0
        if len(self.task.predecessors) > 0:
            for pred in self.task.predecessors:
                pred_end = pred.start_day + pred.get_virtual_duration()
                if pred_end > left_limit:
                    left_limit = pred_end * BAR_SCALE

        if new_x >= 0:
            # Get the nearest successor
            nearest_successor_start = 0
            for task in self.project.tasks:
                if len(task.predecessors) > 0:
                    for task_pred in task.predecessors:
                        if task_pred == self.task:
                            successor_start = task.start_day
                            if successor_start > nearest_successor_start:
                                nearest_successor_start = successor_start

            nearest_successor_x = nearest_successor_start * BAR_SCALE

            new_task_end_x = (int(new_x/BAR_SCALE) + self.task.get_virtual_duration() - 1) * BAR_SCALE

            if self.task.task_segments.index(self.task_segment) == 0:
                if new_x <= left_limit:
                    pass
                else:
                    if nearest_successor_start == 0:
                        self.move_task_segment(new_x)
                    else:
                        if not new_task_end_x >= nearest_successor_x:
                            self.move_task_segment(new_x)
            else:
                # Get the task segment on the left
                ts_index = self.task.task_segments.index(self.task_segment)
                left_ts_index = ts_index - 1
                left_ts: TaskSegment = self.task.task_segments[left_ts_index]
                left_limit = (left_ts.start + left_ts.duration) * BAR_SCALE

                # Move only to the left if it doesn't overlap
                if new_x > left_limit:
                    self.move_task_segment(new_x)

        # TODO Check for update

    def move_task_segment(self, new_x: int):
        self.project.move_task_segment(self.task, self.task_segment, int(new_x / BAR_SCALE))
        self.Move(self.task_segment.start * BAR_SCALE, self.GetPosition()[1])

    def on_hover(self, event):
        pass

    def on_left_up(self, event):
        # Get the task start
        start_x = self.task_segment.start
        self.SetPosition((start_x * BAR_SCALE, self.GetPosition()[1]))

    def on_received_focus(self, event):
        """
        Triggered when the bar is clicked.
        :param event: wx.EVT_LEFT_UP
        """
        res = self.SetBackgroundColour(BG_RECEIVED_FOCUS)
        self.project.selected_task_segment = self.task_segment
        self.project.selected_task = self.task
        self.Refresh()

    def on_lost_focus(self, event):
        """
        Triggered when the mouse is clicked somewhere else or the frame lost
        its focus.
        :param event:
        :return:
        """
        res = self.SetBackgroundColour(BG_DEFAULT)
        self.project.selected_task_segment = None
        self.project.selected_task = None
        self.Refresh()

    def on_double_clicked(self, event):
        task = self.task
        task_segment = self.task_segment

        self.project.selected_task_segment = task_segment
        self.project.selected_task = task

        dlg = SplitTaskDialog(self.parent.parent)

        res = dlg.ShowModal()
        if res == ID_OK:
            dlg.Destroy()
