import wx
import copy


from .constants import *
from ..dialogs.dlg_split_task import SplitTaskDialog

BG_RECEIVED_FOCUS = wx.Colour(0, 0, 0)
BG_DEFAULT = wx.Colour(0, 0, 255)


class BarSegment(wx.Panel):

    task_segment = None
    task = None
    parent = None
    project = None

    def __init__(self, parent, x, y, l, h, task, task_segment):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)

        self.task_segment = task_segment
        self.task = task
        self.parent = parent
        self.project = self.parent.project

        self.SetPosition((x, y))
        self.SetSize(l, h)
        self.SetBackgroundColour(BG_DEFAULT)

        self.SetCursor(wx.Cursor(wx.CURSOR_IBEAM))

        # TRefresh s needed to work on Windows
        self.Refresh()

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_clicked)
        self.Bind(wx.EVT_SET_FOCUS, self.on_received_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_lost_focus)
        # self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_clicked)

    def on_hover(self, event):
        # print('Hovered')
        pass

    def on_left_clicked(self, event):
        self.SetFocus()

    def on_received_focus(self, event):
        """
        Triggered when the bar is clicked.
        :param event: wx.EVT_LEFT_UP
        """
        res = self.SetBackgroundColour(BG_RECEIVED_FOCUS)
        self.project.selected_task_segment = self.task_segment
        self.project.selected_task = self.task
        self.Refresh()

    def on_lost_focus(self, event):
        """
        Triggered when the mouse is clicked somewhere else or the frame lost
        its focus.
        :param event:
        :return:
        """
        res = self.SetBackgroundColour(BG_DEFAULT)
        self.project.selected_task_segment = None
        self.project.selected_task = None
        self.Refresh()

    def on_double_clicked(self, event):
        task = self.task
        task_segment = self.task_segment

        self.project.selected_task_segment = task_segment
        self.project.selected_task = task

        dlg = SplitTaskDialog(self.parent.parent)

        res = dlg.ShowModal()
        if res == ID_OK:
            dlg.Destroy()
