# Import built-in modules
import wx

# Import project modules
from .gantt_chart.task_list import TaskListPane
from .ribbon import Ribbon


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='EasyPlan')
        self.init_ui()
        self.Show()

    def init_ui(self):
        sizer = wx.GridBagSizer(vgap=5, hgap=5)

        ribbon = Ribbon(self)
        sizer.Add(ribbon, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT)

        splitter = wx.SplitterWindow(self)

        left_pane = TaskListPane(splitter)
        right_pane = TaskListPane(splitter)

        splitter.SplitVertically(left_pane, right_pane)

        sizer.Add(splitter, pos=(1, 0),
                  flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM)

        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)
