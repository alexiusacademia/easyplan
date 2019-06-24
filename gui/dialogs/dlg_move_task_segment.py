import wx

from constants import *


class MoveTaskSegmentDialog(wx.Dialog):
    """
    Dialog for moving a task segment.
    """
    project = None
    selected_task = None
    selected_task_segment = None
    parent = None

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.SetTitle('Move Task Segment')

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
        self.add_input('Left Task Duration', main_sizer, str(self.selected_task_segment.start))
        main_sizer.AddSpacer(30)

        split_button = wx.Button(self, ID_OK, label='Move Segment')
        split_button.Bind(wx.EVT_BUTTON, self.on_move_clicked)
        split_button.SetDefault()

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddSpacer(10)
        btn_sizer.Add(split_button)

        main_sizer.Add(btn_sizer)
        main_sizer.AddSpacer(20)

        self.SetSizerAndFit(main_sizer)

    def add_input(self, text, main_sizer, value):
        label = wx.StaticText(self, label=text)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(10)
        sizer.Add(label)
        sizer.AddSpacer(10)
        sizer.Add(wx.TextCtrl(self, name='task_segment_start',
                              style=wx.ALIGN_CENTER_HORIZONTAL, value=value), flag=wx.EXPAND | wx.ALL)
        sizer.AddSpacer(10)

        main_sizer.Add(sizer, flag=wx.EXPAND | wx.ALL)

    def add_title(self, main_sizer):

        instruction = 'Move the task segment at a given day.'

        label = wx.StaticText(self, label=instruction, style=wx.ALIGN_CENTER_HORIZONTAL)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.ITALIC, wx.NORMAL)
        label.SetFont(font)
        label.SetForegroundColour((100, 100, 100))

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.AddSpacer(10)
        sizer.Add(label)
        sizer.AddSpacer(10)

        main_sizer.Add(sizer)

    def on_move_clicked(self, event):
        """
        Move a task segment.
        :param event:
        :return:
        """
        if self.IsModal():
            # Handle the splitting
            new_start_text = self.FindWindowByName('task_segment_start')

            if isinstance(new_start_text, wx.TextCtrl):
                new_start = new_start_text.GetLineText(0)
                if new_start.isdigit():
                    new_start = int(new_start)
                    self.selected_task_segment.move(new_start)
                    self.parent.right_pane.redraw()

                    # Stop the modal state
                    self.EndModal(event.GetEventObject().GetId())
                else:
                    wx.MessageBox('Start day should be an integer.', 'Error', wx.OK | wx.ICON_INFORMATION)

        else:
            self.Close()