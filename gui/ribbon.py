import wx
import wx.ribbon


class Ribbon(wx.ribbon.RibbonBar):
    ribbon_buttons = []

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.create_pages()
        self.set_button_cursors()

    def create_pages(self):
        # ---------------- GANTT CHART PAGE ---------------- #
        gantt_page = wx.ribbon.RibbonPage(self, label='Gantt Chart')

        gantt_panel = wx.Panel(parent=gantt_page)

        gantt_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        # Add task button
        icon_add_task = wx.ArtProvider.GetBitmap(wx.ART_PLUS)
        btn_add_task = wx.BitmapButton(parent=gantt_panel,
                                 bitmap=icon_add_task)
        btn_add_task.SetToolTip(wx.ToolTip('Add new task.'))
        self.Bind(wx.EVT_BUTTON, self.on_add_task, btn_add_task)
        self.ribbon_buttons.append(btn_add_task)
        gantt_page_sizer.Add(btn_add_task, pos=(0, 0))

        icon_indent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD)
        btn_indent_task = wx.BitmapButton(parent=gantt_panel,
                                          bitmap=icon_indent_task)
        btn_indent_task.SetToolTip(wx.ToolTip('Indent task for a single depth.'))
        self.Bind(wx.EVT_BUTTON, self.on_indent_task, btn_indent_task)
        self.ribbon_buttons.append(btn_indent_task)
        gantt_page_sizer.Add(btn_indent_task, pos=(0, 1))

        gantt_panel.SetSizer(gantt_page_sizer)

        # ---------------- GANTT CHART PAGE ---------------- #

        scurve_page = wx.ribbon.RibbonPage(self, label='S-Curve')

        scurve_panel = wx.Panel(parent=scurve_page)
        scurve_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        btn1 = wx.Button(parent=scurve_panel, label='SCurve Button')
        scurve_page_sizer.Add(btn1, pos=(0, 0))

        scurve_panel.SetSizer(scurve_page_sizer)

        self.Realize()

    def set_button_cursors(self):
        for button in self.ribbon_buttons:
            button.SetCursor(wx.Cursor(wx.CURSOR_HAND))

    def on_add_task(self, event):
        print('Add Task')

    def on_indent_task(self, event):
        print('Indent task')