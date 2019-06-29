from wx.lib.docview import Command
import wx


class MoveTaskDownCommand(Command):
    selected_task_index = None
    project = None
    index = None

    def __init__(self, *args, **kw):
        super().__init__()

        self.selected_task_index = args[2]
        self.project = args[3]

    def Do(self):
        self.index = self.project.selected_task_index + 1
        self.project.change_task_index(self.project.selected_task_index, direction=1)

        return True

    def Undo(self):
        self.project.change_task_index(self.index, direction=-1)
        return True