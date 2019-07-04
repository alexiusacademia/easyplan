import wx


class ProjectInformationDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Project Basic Information')

        self.init_ui()

    def init_ui(self):
        pass


class ProjectInformationTB(wx.Treebook):
    def __init__(self, parent, id):
        wx.Treebook.__init__(self,parent, id, style=wx.BK_DEFAULT)

    def create_panel_general(self):
        p = wx.Panel(self, wx.ID_ANY)