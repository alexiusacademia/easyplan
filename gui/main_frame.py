# Import built-in modules
import wx
from pubsub import pub
# Notifications
from pubsub.utils.notification import useNotifyByWriteFile
import sys

# useNotifyByWriteFile(sys.stdout)

from wx.lib.docview import CommandProcessor, Command

# Import project modules
from .gantt_chart.wbs import WBS
from .gantt_chart.gantt import GanttChart
from .ribbon import Ribbon
from core.project import Project
from constants import *


class MainFrame(wx.Frame):
    project = None
    left_pane = None
    right_pane = None
    project_file = ''
    status_bar = None
    command_processor = None

    def __init__(self):
        super().__init__(parent=None, title='EasyPlan')
        self.command_processor = CommandProcessor()
        self.initialize_project()
        self.init_ui()
        self.Show()
        self.Maximize(True)

    def initialize_project(self):
        # self.project = Project()
        pass

    def init_ui(self):
        sizer = wx.GridBagSizer(vgap=5, hgap=5)

        splitter = wx.SplitterWindow(self,
                                     style=wx.SP_3DBORDER | wx.SP_LIVE_UPDATE | wx.SP_3DSASH)
        splitter.SetMinimumPaneSize(400)

        # self.left_pane = TaskListPane(splitter, self.project)
        self.left_pane = WBS(splitter, self.project, self)
        self.right_pane = GanttChart(splitter, self.project, self.left_pane)

        splitter.SplitVertically(self.left_pane, self.right_pane, 400)

        ribbon = Ribbon(self, self.project, self.left_pane)
        sizer.Add(ribbon, pos=(0, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT)

        sizer.Add(splitter, pos=(1, 0),
                  flag=wx.EXPAND | wx.TOP | wx.BOTTOM)

        self.Bind(wx.EVT_SPLITTER_DCLICK, self.on_sash_dbl_clicked)

        self.status_bar = self.CreateStatusBar(2, wx.STB_ELLIPSIZE_MIDDLE)

        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)

    def on_sash_dbl_clicked(self, event):
        print('Splitter has been double clicked.')
