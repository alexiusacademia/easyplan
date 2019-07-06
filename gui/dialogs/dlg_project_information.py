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
        # Controls
        panel = wx.Panel(self)

        label_project_title = wx.StaticText(panel, label='Project Title:', name='project_title')
        entry_project_title = wx.TextCtrl(panel)

        label_project_manager = wx.StaticText(panel, label='Project Manager:', name='project_manager')
        entry_project_manager = wx.TextCtrl(panel)

        label_start_date = wx.StaticText(panel, label='Project Start Date')
        entry_start_date = DatePickerCtrl(panel, -1, style=wx.adv.DP_DROPDOWN)

        # Sizers
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_project_title = wx.BoxSizer(wx.HORIZONTAL)
        sizer_project_manager = wx.BoxSizer(wx.HORIZONTAL)
        sizer_minor_details_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left_main = wx.BoxSizer(wx.VERTICAL)
        sizer_start_date = wx.BoxSizer(wx.HORIZONTAL)

        # Populating each sizer
        sizer_main.Add(sizer_project_title)

        sizer_project_title.AddSpacer(5)
        sizer_project_title.Add(label_project_title, 1)
        sizer_project_title.AddSpacer(46)
        sizer_project_title.Add(entry_project_title, 5)
        sizer_project_title.AddSpacer(5)

        sizer_main.AddSpacer(INPUT_ROW_SPACER)
        sizer_main.Add(sizer_project_manager)

        sizer_project_manager.AddSpacer(5)
        sizer_project_manager.Add(label_project_manager, 1)
        sizer_project_manager.AddSpacer(20)
        sizer_project_manager.Add(entry_project_manager, 2)
        sizer_project_manager.AddSpacer(5)

        sizer_main.AddSpacer(INPUT_ROW_SPACER)
        sizer_main.Add(sizer_minor_details_main, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM | wx.LEFT)

        sizer_left_main.Add(sizer_start_date)

        sizer_start_date.Add(label_start_date, 1)

        if self.start_date is None:
            entry_start_date.SetValue(wx.DateTime.Now())
        else:
            entry_start_date.SetValue(self.start_date)
        sizer_start_date.AddSpacer(LABEL_INPUT_SPACER)
        sizer_start_date.Add(entry_start_date, 1)

        sizer_minor_details_main.AddSpacer(INPUT_GROUP_PADDING)
        sizer_minor_details_main.Add(sizer_left_main, 1)

        panel.SetSizerAndFit(sizer_main)

        return panel

