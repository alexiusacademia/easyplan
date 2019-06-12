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

        self.SetPosition(((int(task.start_day) - 1) * hor_scale, y))
        self.Size = wx.Size(task.get_virtual_duration() * hor_scale, self.BAR_THICKNESS)
        self.SetBackgroundColour(wx.BLUE)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_hover)

    def on_mouse_hover(self, event):
        print('h')
