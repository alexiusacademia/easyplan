import wx
import copy


from .constants import *


class BarSegment(wx.Panel):

    task_segment = None
    task = None
    parent = None

    def __init__(self, parent, x, y, l, h, task, task_segment):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)

        self.task_segment = task_segment
        self.task = task
        self.parent = parent

        self.SetPosition((x, y))
        self.SetSize(l, h)
        self.SetBackgroundColour(wx.BLUE)

        self.SetCursor(wx.Cursor(wx.CURSOR_IBEAM))

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        #self.Bind(wx.EVT_LEFT_DCLICK,
        #          lambda event, t=task, ts=task_segment: self.on_double_clicked(event, t, ts))

    def on_hover(self, event):
        # print('Hovered')
        pass
