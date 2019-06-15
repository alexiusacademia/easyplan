import wx

from ..gantt_chart.constants import *


class SplitTaskDialog(wx.Dialog):
    project = None

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Split Task')

        self.project = parent.project

        self.init_ui()
        # self.ShowModal()

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(10)

        self.add_title(main_sizer)

        main_sizer.AddSpacer(30)
        self.add_input('Left Task Duration', main_sizer)
        main_sizer.AddSpacer(30)

        split_button = wx.Button(self, ID_OK, label='Split Task')
        split_button.Bind(wx.EVT_BUTTON, self.on_split_clicked)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddSpacer(10)
        btn_sizer.Add(split_button)

        main_sizer.Add(btn_sizer)
        main_sizer.AddSpacer(20)

        self.SetSizerAndFit(main_sizer)

    def add_input(self, text, main_sizer):
        label = wx.StaticText(self, label=text)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(10)
        sizer.Add(label)
        sizer.AddSpacer(10)
        sizer.Add(wx.TextCtrl(self, name='left_duration', style=wx.ALIGN_CENTER_HORIZONTAL), flag=wx.EXPAND | wx.ALL)
        sizer.AddSpacer(10)

        main_sizer.Add(sizer, flag=wx.EXPAND | wx.ALL)

    def add_title(self, main_sizer):
        title = 'Specify the duration of the resulting task segment on the left.\n' \
                'The right segment will have the difference of the left segment and the original task segment.'

        label = wx.StaticText(self, label=title, style=wx.ALIGN_CENTER_HORIZONTAL)
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.ITALIC, wx.NORMAL)
        label.SetFont(font)
        label.SetForegroundColour((100, 100, 100))

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(10)
        sizer.Add(label)
        sizer.AddSpacer(10)

        main_sizer.Add(sizer)

    def on_split_clicked(self, event):
        if self.IsModal():
            self.EndModal(event.GetEventObject().GetId())
        else:
            self.Close()