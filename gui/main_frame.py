import wx


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Test')
        self.Show()