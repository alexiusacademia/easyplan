import wx


class ProjectInformationDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Project Basic Information')
