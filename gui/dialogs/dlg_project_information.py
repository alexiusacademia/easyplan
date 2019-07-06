import wx
from wx.adv import DatePickerCtrl

INPUT_ROW_SPACER = 10
INPUT_GROUP_PADDING = 20
LABEL_INPUT_SPACER = 20


class ProjectInformationDialog(wx.Dialog):

    start_date = None

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Basic Project Information')

        self.init_ui()

    def init_ui(self):
        nb = ProjectInformationNB(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(nb)

        self.SetSizerAndFit(sizer)


class ProjectInformationNB(wx.Notebook):

    start_date = None

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)

        self.AddPage(self.general_panel(), 'General Information')
        self.start_date = parent.start_date

    def general_panel(self):
        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        project_title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(project_title_sizer)

        label_project_title = wx.StaticText(panel, label='Project Title:', name='project_title')
        entry_project_title = wx.TextCtrl(panel)

        project_title_sizer.AddSpacer(5)
        project_title_sizer.Add(label_project_title, 1)
        project_title_sizer.AddSpacer(46)
        project_title_sizer.Add(entry_project_title, 5)
        project_title_sizer.AddSpacer(5)

        project_manager_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.AddSpacer(INPUT_ROW_SPACER)
        main_sizer.Add(project_manager_sizer)

        label_project_manager = wx.StaticText(panel, label='Project Manager:', name='project_manager')
        entry_project_manager = wx.TextCtrl(panel)

        project_manager_sizer.AddSpacer(5)
        project_manager_sizer.Add(label_project_manager, 1)
        project_manager_sizer.AddSpacer(20)
        project_manager_sizer.Add(entry_project_manager, 2)
        project_manager_sizer.AddSpacer(5)

        minor_details_main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.AddSpacer(INPUT_ROW_SPACER)
        main_sizer.Add(minor_details_main_sizer, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM | wx.LEFT)

        left_minor_panel = wx.Panel(panel)
        minor_details_main_sizer.AddSpacer(INPUT_GROUP_PADDING)
        minor_details_main_sizer.Add(left_minor_panel, 1)

        right_minor_panel = wx.Panel(panel)
        minor_details_main_sizer.Add(right_minor_panel, 1)
        minor_details_main_sizer.AddSpacer(INPUT_GROUP_PADDING)

        sizer_start_date = wx.BoxSizer(wx.HORIZONTAL)
        label_start_date = wx.StaticText(left_minor_panel, label='Start Date')
        sizer_start_date.Add(label_start_date, 1)
        entry_start_date = DatePickerCtrl(right_minor_panel, -1, style=wx.adv.DP_DROPDOWN)
        if self.start_date is None:
            entry_start_date.SetValue(wx.DateTime.Now())
        else:
            entry_start_date.SetValue(self.start_date)
        sizer_start_date.AddSpacer(LABEL_INPUT_SPACER)
        sizer_start_date.Add(entry_start_date, 1)

        panel.SetSizerAndFit(main_sizer)

        return panel

