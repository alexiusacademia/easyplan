# Import built-in modules
import wx

# Import project modules
from gui.main_frame import MainFrame


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()