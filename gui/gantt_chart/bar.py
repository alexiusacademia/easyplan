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

        self.on_paint()

    def on_paint(self,):
        dc = wx.PaintDC(self.parent)
        dc.SetBrush(wx.Brush(wx.BLUE))
        dc.DrawRectangle((int(self.task.start_day) - 1) * self.hor_scale,
                         self.y,
                         self.task.get_virtual_duration() * self.hor_scale,
                         self.BAR_THICKNESS)
