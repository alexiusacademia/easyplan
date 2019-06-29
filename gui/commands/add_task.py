from wx.lib.docview import Command


class AddTaskCommand(Command):
    """
    Implements a command on the undo/redo stack.
    """
    task = None
    selected_task_index = None
    project = None

    def __init__(self, *args, **kw):
        """
        Implements a command on the undo/redo stack.
        """
        super().__init__()

        self.task = args[2]
        self.selected_task_index = args[3]
        self.project = args[4]

    def Do(self):
        if self.selected_task_index is not None:
            index = self.selected_task_index
            self.project.insert_task(index, self.task)
        else:
            self.project.add_task(self.task)
        self.project.selected_task_index = None
        return True

    def Undo(self):
        self.project.remove_task(self.task)
        return True