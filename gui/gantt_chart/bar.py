import wx


class Bar(wx.Window):
    task = None

    BAR_THICKNESS = 20

    def __init__(self, parent, task, y, hor_scale):
        wx.Window.__init__(self, parent)

        self.parent = parent
        self.task = task
        self.y = y
        self.hor_scale = hor_scale

        #self.SetPosition(((int(task.start_day) - 1) * hor_scale, y))
        #self.Size = wx.Size(task.get_virtual_duration() * hor_scale, self.BAR_THICKNESS)
        #self.SetBackgroundColour(wx.BLUE)
        for ts in task.task_segments:
            bs = BarSegment(parent, ts.start, ts.duration, y, hor_scale)


class BarSegment(wx.Panel):
    def __init__(self, parent, x, y, l, h):
        wx.Panel.__init__(self, parent)

        self.SetPosition((x, y))
        self.SetSize(l, h)
        self.SetBackgroundColour(wx.GREEN)

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)

    def on_hover(self, event):
        print('Hovered')