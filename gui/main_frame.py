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
from .accelerators import *


class MainFrame(wx.Frame):
    project = None
    left_pane = None
    right_pane = None
    project_file = ''
    status_bar = None
    command_processor = None
    ribbon = None

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
        self.ribbon = ribbon

        sizer.Add(splitter, pos=(1, 0),
                  flag=wx.EXPAND | wx.TOP | wx.BOTTOM)

        self.Bind(wx.EVT_SPLITTER_DCLICK, self.on_sash_dbl_clicked)

        self.status_bar = self.CreateStatusBar(2, wx.STB_ELLIPSIZE_MIDDLE)

        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(0)

        self.SetSizer(sizer)

        self.set_bindings()

    def set_bindings(self):
        self.Bind(wx.EVT_MENU, self.ribbon.on_undo, id=AcceleratorIds.CTRL_Z)
        self.Bind(wx.EVT_MENU, self.ribbon.on_redo, id=AcceleratorIds.CTRL_Y)
        self.Bind(wx.EVT_MENU, self.ribbon.on_delete_task, id=AcceleratorIds.CTRL_SHIFT_DEL)
        self.Bind(wx.EVT_MENU, self.ribbon.on_add_task, id=AcceleratorIds.CTRL_SHIFT_PLUS)
        self.Bind(wx.EVT_MENU, self.ribbon.on_save_project, id=AcceleratorIds.CTRL_S)
        self.Bind(wx.EVT_MENU, self.ribbon.on_open_project, id=AcceleratorIds.CTRL_O)
        self.Bind(wx.EVT_MENU, self.ribbon.on_new_project, id=AcceleratorIds.CTRL_N)
        self.Bind(wx.EVT_MENU, self.ribbon.on_split_task, id=AcceleratorIds.CTRL_T)
        self.Bind(wx.EVT_MENU, self.ribbon.on_move_segment, id=AcceleratorIds.CTRL_SHIFT_S)
        self.Bind(wx.EVT_MENU, self.ribbon.on_merge_segments, id=AcceleratorIds.CTRL_M)
        self.SetAcceleratorTable(accelerator_table)

    def on_sash_dbl_clicked(self, event):
        print('Splitter has been double clicked.')
