from wx.lib.docview import Command
import wx
from pubsub import pub
import copy

from core.task import Task
from core.task_segment import TaskSegment
from constants import *


class MergeTaskSegments(Command):
    task = None
    old_task_segments = []
    old_task = None

    def __init__(self, *args, **kw):
        """
        Implements a command on the undo/redo stack.
        """
        super().__init__()

        self.task: Task = args[2]

        for task_segment in self.task.task_segments:
            self.old_task_segments.append(copy.copy(task_segment))

        self.old_task = copy.copy(args[2])

    def Do(self):

        result = self.task.merge_task_segments()
        if result[0]:
            pub.sendMessage(EVENT_PROJECT_UPDATED)
        else:
            wx.MessageBox('No merging necessary.', 'Merge Task Segments',
                          wx.OK | wx.CENTER)
        return True

    def Undo(self):
        self.task.task_segments.clear()

        for task_segment in self.old_task_segments:
            self.task.task_segments.append(copy.copy(task_segment))

        pub.sendMessage(EVENT_PROJECT_UPDATED)

        return True
