from wx.lib.docview import Command

from core.task_segment import TaskSegment
from core.project import Project
from core.task import Task


class MoveTaskSegmentCommand(Command):

    old_start = None
    new_start = None
    task = None
    selected_task_segment = None
    project = None

    def __init__(self, *args, **kw):
        super().__init__()

        self.new_start: int = args[2]
        self.task: Task = args[3]
        self.selected_task_segment: TaskSegment = args[4]
        self.old_start = self.selected_task_segment.start
        self.project: Project = args[5]

    def Do(self):
        # self.selected_task_segment.move(self.new_start)
        self.project.move_task_segment(self.task, self.selected_task_segment, self.new_start)
        # self.project.update_successors()
        return True

    def Undo(self):
        self.project.move_task_segment(self.task, self.selected_task_segment, self.old_start)
        return True
