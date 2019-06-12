import wx


class Bar(wx.Window):
    def __init__(self, parent, x, y, thickness, duration):
        wx.Window.__init__(self, parent)

        dc = wx.PaintDC(parent)
        dc.SetBrush(wx.Brush(wx.BLUE))
        dc.DrawRectangle(x, y, duration, thickness)
