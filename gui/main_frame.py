# Import built-in modules
import wx
from wx.lib.splitter import MultiSplitterWindow

# Import project modules
from .gantt_chart.task_list import TaskListPane
from .ribbon import Ribbon
from core.project import Project


class MainFrame(wx.Frame):
    project = None

    def __init__(self):
        super().__init__(parent=None, title='EasyPlan')
        self.initialize_project()
        self.init_ui()
        self.Show()
        self.Maximize(True)

    def initialize_project(self):
        self.project = Project()
        self.project.project_name = 'Untitled project.'

    def init_ui(self):
        sizer = wx.GridBagSizer(vgap=5, hgap=5)

        splitter = wx.SplitterWindow(self,
                                     style=wx.SP_THIN_SASH | wx.NO_BORDER | wx.SP_3D | wx.SP_LIVE_UPDATE)
        splitter.SetMinimumPaneSize(400)

        self.left_pane = TaskListPane(splitter, self.project)
        right_pane = TaskListPane(splitter, self.project)

        splitter.SplitVertically(self.left_pane, right_pane, 400)

        ribbon = Ribbon(self, self.project)
        sizer.Add(ribbon, pos=(0, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT)

        sizer.Add(splitter, pos=(1, 0),
                  flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM)

        self.Bind(wx.EVT_SPLITTER_DCLICK, self.on_sash_dbl_clicked)

        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)

    def refresh(self):
        self.left_pane.redraw_project()

    def on_sash_dbl_clicked(self, event):
        print(event)
