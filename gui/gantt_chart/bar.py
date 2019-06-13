import wx


class BarSegment(wx.Panel):
    def __init__(self, parent, x, y, l, h):
        wx.Panel.__init__(self, parent)

        self.SetPosition((x, y))
        self.SetSize(l, h)
        self.SetBackgroundColour(wx.GREEN)

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)

    def on_hover(self, event):
        print('Hovered')