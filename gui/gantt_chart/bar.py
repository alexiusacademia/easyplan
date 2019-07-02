import wx
from wx.lib.docview import CommandProcessor

from constants import *
from ..dialogs.dlg_split_task import SplitTaskDialog
from core.task_segment import TaskSegment
from core.project import Project

from ..commands.move_task_segment_by_dragging import MoveTaskSegmentCommand

BG_RECEIVED_FOCUS = wx.Colour(0, 0, 0)
BG_DEFAULT = wx.Colour(0, 0, 255)


class BarSegment(wx.Panel):

    task_segment = None
    task = None
    parent = None
    project = None
    command_processor = None

    left_limit = 0
    right_limit = 1000000

    def __init__(self, parent, x, y, l, h, task, task_segment):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)

        self.task_segment: TaskSegment = task_segment
        self.task = task
        self.parent = parent
        self.command_processor: CommandProcessor = parent.parent.command_processor
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

        # Get the left limit for predecessor
        if len(self.task.predecessors) > 0:
            for pred in self.task.predecessors:
                pred_end = pred.get_finish() * BAR_SCALE
                if pred_end > self.left_limit:
                    self.left_limit = pred_end

        # Get the left limit for split tasks
        ts_index = self.task.task_segments.index(self.task_segment)
        if ts_index != 0:
            # Get the task segment on the left
            left_ts_index = ts_index - 1
            left_ts: TaskSegment = self.task.task_segments[left_ts_index]
            left_limit = left_ts.get_finish() * BAR_SCALE
            if left_limit > self.left_limit:
                self.left_limit = left_limit

        # Get right limit for successors
        # Get the nearest successor
        nearest_successor_start = 1000000
        for task in self.project.tasks:
            if len(task.predecessors) > 0:
                for task_pred in task.predecessors:
                    if task_pred == self.task:
                        successor_start = task.start_day
                        if successor_start < nearest_successor_start:
                            nearest_successor_start = successor_start
        nearest_successor_location = nearest_successor_start * BAR_SCALE
        if nearest_successor_location < self.right_limit:
            self.right_limit = nearest_successor_location

        # Get the right limit for splitted task
        if ts_index < (len(self.task.task_segments) - 1):
            # There is a segment to the right
            right_ts: TaskSegment = self.task.task_segments[ts_index + 1]
            right_limit = right_ts.start * BAR_SCALE
            if right_limit < self.right_limit:
                self.right_limit = right_limit

    def on_mouse_move(self, event):
        if not event.Dragging or not event.LeftIsDown():
            return

        # Get the bar's current position
        starting_point = self.GetPosition()[0]

        # Initial mouse position
        start_x = self.mouse_start_position

        dx = (event.GetPosition()[0] - start_x)

        new_x = starting_point + dx

        if new_x >= 0 and abs(dx) >= BAR_SCALE:
            # The calculated/predicted location of the tip of this task segment bar.
            new_task_end_x = (int(new_x/BAR_SCALE) + self.task_segment.duration - 1) * BAR_SCALE

            if (new_x + BAR_SCALE) > self.left_limit and \
                    (new_task_end_x + BAR_SCALE) < self.right_limit:
                self.move_task_segment(new_x)

    def move_task_segment(self, new_x: int):
        # self.project.move_task_segment(self.task, self.task_segment, int(new_x / BAR_SCALE))
        command = MoveTaskSegmentCommand(True, 'Move Task Segment',
                                         int(new_x / BAR_SCALE),
                                         self.task,
                                         self.task_segment,
                                         self.project,
                                         self)
        self.command_processor.Submit(command)
        # self.Move(self.task_segment.start * BAR_SCALE, self.GetPosition()[1])

    def on_hover(self, event):
        pass

    def on_left_up(self, event):
        # Get the task start
        start_x = self.task_segment.start - 1
        self.SetPosition((start_x * BAR_SCALE, self.GetPosition()[1]))

    def on_received_focus(self, event):
        """
        Triggered when the bar is clicked.
        :param event: wx.EVT_LEFT_UP
        """
        res = self.SetBackgroundColour(BG_RECEIVED_FOCUS)
        self.project.selected_task_segment = self.task_segment
        self.project.selected_task = self.task
        self.project.selected_task_index = self.project.tasks.index(self.task)
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
