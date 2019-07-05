import wx


class ProjectInformationDialog(wx.Dialog):
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
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)

        self.AddPage(self.general_panel(), 'General Information')

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
        main_sizer.AddSpacer(10)
        main_sizer.Add(project_manager_sizer)

        label_project_manager = wx.StaticText(panel, label='Project Manager:', name='project_manager')
        entry_project_manager = wx.TextCtrl(panel)

        project_manager_sizer.AddSpacer(5)
        project_manager_sizer.Add(label_project_manager, 1)
        project_manager_sizer.AddSpacer(20)
        project_manager_sizer.Add(entry_project_manager, 2)
        project_manager_sizer.AddSpacer(5)

        panel.SetSizerAndFit(main_sizer)

        return panel

