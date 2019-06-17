import wx

from ..gantt_chart.constants import *


class SplitTaskDialog(wx.Dialog):
    project = None
    selected_task = None
    selected_task_segment = None
    parent = None

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Split Task')

        self.project = parent.project
        self.selected_task = self.project.selected_task
        self.selected_task_segment = self.project.selected_task_segment
        self.parent = parent

        self.init_ui()

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.AddSpacer(10)

        self.add_title(main_sizer)

        main_sizer.AddSpacer(30)
        self.add_input('Left Task Duration', main_sizer)
        main_sizer.AddSpacer(30)

        split_button = wx.Button(self, ID_OK, label='Split Task')
        split_button.Bind(wx.EVT_BUTTON, self.on_split_clicked)
        split_button.SetDefault()

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
                'The right segment will have the difference \nof the left segment and the original task segment.'

        label = wx.StaticText(self, label=title, style=wx.ALIGN_CENTER_HORIZONTAL)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.ITALIC, wx.NORMAL)
        label.SetFont(font)
        label.SetForegroundColour((100, 100, 100))

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(10)
        sizer.Add(label)
        sizer.AddSpacer(10)

        main_sizer.Add(sizer)

    def on_split_clicked(self, event):
        if self.IsModal():
            # Handle the splitting
            input_left = self.FindWindowByName('left_duration')

            if isinstance(input_left, wx.TextCtrl):
                left_duration = input_left.GetLineText(0)
                if left_duration.isdigit():
                    left_duration = int(left_duration)
                    self.selected_task.split_task(self.selected_task_segment, left_duration)

                    self.parent.right_pane.redraw()

                else:
                    wx.MessageBox('Left duration should be an integer.', 'Error', wx.OK | wx.ICON_INFORMATION)

            # Stop the modal state
            self.EndModal(event.GetEventObject().GetId())

        else:
            self.Close()