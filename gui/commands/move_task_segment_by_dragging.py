from wx.lib.docview import Command
from pubsub import pub

from core.task_segment import TaskSegment
from core.project import Project
from core.task import Task
from constants import *


class MoveTaskSegmentCommand(Command):

    old_start = None
    new_start = None
    task = None
    selected_task_segment = None
    project = None
    bar_segment = None

    def __init__(self, *args, **kw):
        super().__init__()

        self.new_start: int = args[2]
        self.task: Task = args[3]
        self.selected_task_segment: TaskSegment = args[4]
        self.old_start = self.selected_task_segment.start
        self.project: Project = args[5]
        self.bar_segment = args[6]

    def Do(self):
        self.project.move_task_segment(self.task, self.selected_task_segment, self.new_start)
        self.bar_segment.Move(self.selected_task_segment.start * BAR_SCALE, self.bar_segment.GetPosition()[1])
        pub.sendMessage(EVENT_BAR_SEGMENT_MOVING,
                        task=self.task,
                        task_segment=self.selected_task_segment,
                        task_start=self.new_start)
        return True

    def Undo(self):
        self.project.move_task_segment(self.task, self.selected_task_segment, self.old_start)
        self.bar_segment.Move(self.selected_task_segment.start * BAR_SCALE, self.bar_segment.GetPosition()[1])
        pub.sendMessage(EVENT_BAR_SEGMENT_MOVING,
                        task=self.task,
                        task_segment=self.selected_task_segment,
                        task_start=self.old_start)
        return True
