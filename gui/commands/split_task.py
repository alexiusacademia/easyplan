from wx.lib.docview import Command

from core.task import Task
from core.task_segment import TaskSegment


class SplitTaskCommand(Command):
    left_duration = None
    selected_task = None
    selected_task_segment = None
    project = None

    result = None

    def __init__(self, *args, **kw):
        super().__init__()

        self.left_duration = args[2]
        self.selected_task: Task = args[3]
        self.selected_task_segment: TaskSegment = args[4]
        self.project = args[5]

    def Do(self):
        left_duration = int(self.left_duration)
        result = self.selected_task.split_task(self.selected_task_segment, left_duration)
        self.result = result

        self.project.update_successors()
        return True

    def Undo(self):
        self.selected_task.undo_split_task(self.selected_task_segment,
                                           self.result[1][0],
                                           self.result[1][1])

        self.project.update_successors()
        return True