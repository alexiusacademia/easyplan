import wx
import copy


from .constants import *

BG_RECEIVED_FOCUS = wx.BLACK
BG_DEFAULT = wx.BLUE

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

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_clicked)
        self.Bind(wx.EVT_SET_FOCUS, self.on_received_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_lost_focus)
        #self.Bind(wx.EVT_LEFT_DCLICK,
        #          lambda event, t=task, ts=task_segment: self.on_double_clicked(event, t, ts))

    def on_hover(self, event):
        # print('Hovered')
        pass

    def on_left_clicked(self, event):
        self.SetFocus()

    def on_received_focus(self, event):
        res = self.SetBackgroundColour(BG_RECEIVED_FOCUS)
        self.project.selected_task_segment = self.task_segment
        self.project.selected_task = self.task
        self.Refresh()

    def on_lost_focus(self, event):
        res = self.SetBackgroundColour(BG_DEFAULT)
        self.project.selected_task_segment = None
        self.project.selected_task = None
        self.Refresh()
