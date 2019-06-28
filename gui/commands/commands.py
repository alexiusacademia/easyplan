from wx.lib.docview import Command
import wx.richtext
import wx


class MoveTaskUpCommand(Command):
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

            if index == 0:
                pass
            else:
                self.index = index - 1
                self.project.change_task_index(index, direction=-1)

        return True

    def Undo(self):
        self.project.change_task_index(self.index, direction=1)
        return True


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
