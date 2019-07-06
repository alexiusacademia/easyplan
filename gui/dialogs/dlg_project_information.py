import wx
from wx.adv import DatePickerCtrl

from core.project import Project

INPUT_ROW_SPACER = 10
INPUT_GROUP_PADDING = 20
LABEL_INPUT_SPACER = 20


class ProjectInformationDialog(wx.Dialog):

    project = None

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Basic Project Information')
        self.project = parent.project

        self.init_ui()

    def init_ui(self):
        nb = ProjectInformationNB(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(nb)

        self.SetSizerAndFit(sizer)


class ProjectInformationNB(wx.Notebook):

    start_date = None
    project = None

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)

        project: Project = parent.project
        self.project = project

        self.start_date = project.start_date

        self.AddPage(self.general_panel(), 'General Information')

    def general_panel(self):
        # --------------------
        # Controls
        # --------------------
        panel = wx.Panel(self)

        label_project_title = wx.StaticText(panel, label='Project Title', name='project_title')
        entry_project_title = wx.TextCtrl(panel)

        label_project_manager = wx.StaticText(panel, label='Project Manager', name='project_manager')
        entry_project_manager = wx.TextCtrl(panel)

        label_start_date = wx.StaticText(panel, label='Start Date')
        entry_start_date = DatePickerCtrl(panel, -1, style=wx.adv.DP_DROPDOWN)
        if self.start_date is None:
            entry_start_date.SetValue(wx.DateTime.Now())
        else:
            entry_start_date.SetValue(self.start_date)

        label_finish_date = wx.StaticText(panel, label='Finish Date')
        entry_finish_date = DatePickerCtrl(panel, -1, style=wx.adv.DP_DROPDOWN)

        duration = self.project.get_project_duration()
        date_span = wx.DateSpan(0, 0, 0, int(duration) - 1)
        date_finish = self.project.start_date.Add(date_span)
        entry_finish_date.SetValue(date_finish)
        entry_finish_date.Disable()


        # --------------------
        # Sizers
        # --------------------
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_project_title = wx.BoxSizer(wx.HORIZONTAL)
        sizer_project_manager = wx.BoxSizer(wx.HORIZONTAL)
        sizer_minor_details_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left_main = wx.BoxSizer(wx.VERTICAL)
        sizer_start_date = wx.BoxSizer(wx.HORIZONTAL)
        sizer_finish_date = wx.BoxSizer(wx.HORIZONTAL)

        # --------------------
        # Populating each sizer
        # --------------------
        sizer_main.Add(sizer_project_title)

        sizer_project_title.AddSpacer(INPUT_GROUP_PADDING)
        sizer_project_title.Add(label_project_title, 1)
        sizer_project_title.AddSpacer(46)
        sizer_project_title.Add(entry_project_title, 5)
        sizer_project_title.AddSpacer(INPUT_GROUP_PADDING)

        sizer_main.AddSpacer(INPUT_ROW_SPACER)
        sizer_main.Add(sizer_project_manager)

        sizer_project_manager.AddSpacer(INPUT_GROUP_PADDING)
        sizer_project_manager.Add(label_project_manager, 1)
        sizer_project_manager.AddSpacer(20)
        sizer_project_manager.Add(entry_project_manager, 2)
        sizer_project_manager.AddSpacer(INPUT_GROUP_PADDING)

        sizer_main.AddSpacer(INPUT_ROW_SPACER)
        sizer_main.Add(sizer_minor_details_main, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM | wx.LEFT)

        sizer_left_main.Add(sizer_start_date)
        sizer_left_main.Add(sizer_finish_date)

        sizer_start_date.Add(label_start_date, .5)
        sizer_start_date.AddSpacer(59)
        sizer_start_date.Add(entry_start_date, 1)

        sizer_finish_date.Add(label_finish_date, .5)
        sizer_finish_date.AddSpacer(53)
        sizer_finish_date.Add(entry_finish_date)

        sizer_minor_details_main.AddSpacer(INPUT_GROUP_PADDING)
        sizer_minor_details_main.Add(sizer_left_main, 1)

        panel.SetSizerAndFit(sizer_main)

        return panel

