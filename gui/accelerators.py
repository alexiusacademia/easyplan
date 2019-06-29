import wx


class AcceleratorIds:
    CTRL_Z = 1000
    CTRL_Y = 1001
    DEL = 1002


accelerator_table = wx.AcceleratorTable([
    (wx.ACCEL_CTRL, ord('Z'), AcceleratorIds.CTRL_Z),
    (wx.ACCEL_CTRL, ord('Y'), AcceleratorIds.CTRL_Y),
    (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('-'), AcceleratorIds.DEL)
])