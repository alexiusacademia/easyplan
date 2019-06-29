from wx.lib.docview import Command
import wx.richtext
import wx


class SplitTaskCommand(Command):
    left_duration = None
    selected_task = None
    selected_task_segment = None
    project = None

    def __init__(self, *args, **kw):
        super().__init__()

        self.left_duration = args[2]
        self.selected_task = args[3]
        self.selected_task_segment = args[4]
        self.project = args[5]

    def Do(self):
        left_duration = int(self.left_duration)
        self.selected_task.split_task(self.selected_task_segment, left_duration)
        self.project.update_successors()

        return True

    def Undo(self):
        # TODO Undo split task
        return True
