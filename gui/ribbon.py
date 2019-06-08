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

        # -- Task Panel -- #
        gantt_task_panel = wx.ribbon.RibbonPanel(parent=gantt_page, label='',
                                            style=wx.ribbon.RIBBON_PANEL_DEFAULT_STYLE)

        gantt_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        # Add task button
        pos = 0
        icon_add_task = wx.ArtProvider.GetBitmap(wx.ART_PLUS)
        btn_add_task = wx.BitmapButton(parent=gantt_task_panel, bitmap=icon_add_task)
        btn_add_task.SetToolTip(wx.ToolTip('Add new task.'))
        self.Bind(wx.EVT_BUTTON, self.on_add_task, btn_add_task)
        self.ribbon_buttons.append(btn_add_task)
        gantt_page_sizer.Add(btn_add_task, pos=(0, pos))

        # Outdent task button
        pos += 1
        icon_outdent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK)
        btn_outdent_task = wx.BitmapButton(parent=gantt_task_panel, bitmap=icon_outdent_task)
        btn_outdent_task.SetToolTip(wx.ToolTip('Remove single indent.'))
        self.ribbon_buttons.append(btn_outdent_task)
        gantt_page_sizer.Add(btn_outdent_task, pos=(0, pos))

        # Indent task button
        pos += 1
        icon_indent_task = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD)
        btn_indent_task = wx.BitmapButton(parent=gantt_task_panel, bitmap=icon_indent_task)
        btn_indent_task.SetToolTip(wx.ToolTip('Indent task for a single depth.'))
        self.Bind(wx.EVT_BUTTON, self.on_indent_task, btn_indent_task)
        self.ribbon_buttons.append(btn_indent_task)
        gantt_page_sizer.Add(btn_indent_task, pos=(0, pos))

        # Delete task button
        pos += 1
        icon_delete_task = self.get_stock_bitmap(wx.ART_MINUS)
        btn_delete_task = wx.BitmapButton(parent=gantt_task_panel, bitmap=icon_delete_task)
        btn_delete_task.SetToolTip(wx.ToolTip('Delete task.'))
        self.ribbon_buttons.append(btn_delete_task)
        gantt_page_sizer.Add(btn_delete_task, pos=(0, pos))

        gantt_task_panel.SetSizer(gantt_page_sizer)
        # -- End Task Panel -- #

        # ---------------- GANTT CHART PAGE ---------------- #

        scurve_page = wx.ribbon.RibbonPage(self, label='S-Curve')

        scurve_panel = wx.Panel(parent=scurve_page)
        scurve_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        btn1 = wx.Button(parent=scurve_panel, label='SCurve Button')
        scurve_page_sizer.Add(btn1, pos=(0, 0))

        scurve_panel.SetSizer(scurve_page_sizer)

        self.Realize()

    def get_stock_bitmap(self, art_id):
        return wx.ArtProvider.GetBitmap(art_id)

    def set_button_cursors(self):
        for button in self.ribbon_buttons:
            button.SetCursor(wx.Cursor(wx.CURSOR_HAND))

    def on_add_task(self, event):
        print('Add Task')

    def on_outdent_task(self, event):
        print('Outdent Task')

    def on_indent_task(self, event):
        print('Indent task')

    def on_delete_task(self, event):
        print('Delete task.')
