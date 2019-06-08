import wx
import wx.ribbon


class Ribbon(wx.ribbon.RibbonBar):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.create_pages()
        self.Realize()

    def create_pages(self):
        ############# GANTT CHART PAGE ################
        gantt_page = wx.ribbon.RibbonPage(self, label='Gantt Chart')

        gantt_panel = wx.Panel(parent=gantt_page)
        gantt_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        btn_test = wx.Button(parent=gantt_panel, label='Test Button')
        gantt_page_sizer.Add(btn_test, pos=(0, 0))

        gantt_panel.SetSizer(gantt_page_sizer)

        ############# GANTT CHART PAGE ################

        scurve_page = wx.ribbon.RibbonPage(self, label='S-Curve')

        scurve_panel = wx.Panel(parent=scurve_page)
        scurve_page_sizer = wx.GridBagSizer(vgap=0, hgap=0)

        btn1 = wx.Button(parent=scurve_panel, label='SCurve Button')
        scurve_page_sizer.Add(btn1, pos=(0, 0))

        scurve_panel.SetSizer(scurve_page_sizer)
