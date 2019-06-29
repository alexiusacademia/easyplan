from wx.lib.docview import Command
import wx
from pubsub import pub
from constants import *


class RemoveTaskCommand(Command):
    task = None
    selected_task_index = None
    project = None
    successors = None

    def __init__(self, *args, **kw):
        super().__init__()

        self.task = args[2]
        self.selected_task_index = args[3]
        self.project = args[4]
        self.successors = args[5]

    def Do(self):
        if self.project.selected_task_index is None:
            wx.MessageBox('A task shall be selected from the WBS before deleting.', 'No Task Selected',
                          style=wx.OK_DEFAULT)
        else:
            # Ask user for confirmation
            index = self.project.selected_task_index

            if index <= len(self.project.tasks) - 1:
                dlg = wx.MessageBox('Delete the selected task?', 'Delete Task', style=wx.YES_NO | wx.CANCEL)
                if dlg == wx.YES:
                    self.project.remove_task(self.project.tasks[index])
                    self.project.selected_task_index = None
        return True

    def Undo(self):
        if self.selected_task_index is not None:
            index = self.selected_task_index
            self.project.insert_task(index, self.task)
        else:
            self.project.add_task(self.task)
        self.project.selected_task_index = self.selected_task_index

        # Restore successors dependents
        for successor in self.successors:
            successor.predecessors.append(self.task)

        pub.sendMessage(EVENT_PROJECT_UPDATED)

        return True