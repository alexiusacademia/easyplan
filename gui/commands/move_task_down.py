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
        if self.project.selected_task_index is None:
            wx.MessageBox('A task shall be selected from the WBS before moving.', 'No Task Selected',
                          style=wx.OK_DEFAULT)
        else:
            index = self.project.selected_task_index

            if index == len(self.project.tasks) - 1:
                pass
            else:
                self.index = index + 1
                self.project.change_task_index(index, direction=1)

        return True

    def Undo(self):
        self.project.change_task_index(self.index, direction=-1)
        return True