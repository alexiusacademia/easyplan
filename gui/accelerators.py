import wx


class AcceleratorIds:
    CTRL_Z = 1000
    CTRL_Y = 1001

    CTRL_SHIFT_DEL = 1002
    CTRL_SHIFT_PLUS = 1003

    CTRL_S = 1004
    CTRL_O = 1005
    CTRL_N = 1006

    CTRL_T = 1009
    CTRL_SHIFT_S = 1010


accelerator_table = wx.AcceleratorTable([
    (wx.ACCEL_CTRL, ord('Z'), AcceleratorIds.CTRL_Z),
    (wx.ACCEL_CTRL, ord('Y'), AcceleratorIds.CTRL_Y),

    (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('-'), AcceleratorIds.CTRL_SHIFT_DEL),
    (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('='), AcceleratorIds.CTRL_SHIFT_PLUS),

    (wx.ACCEL_CTRL, ord('S'), AcceleratorIds.CTRL_S),
    (wx.ACCEL_CTRL, ord('O'), AcceleratorIds.CTRL_O),
    (wx.ACCEL_CTRL, ord('N'), AcceleratorIds.CTRL_N),

    (wx.ACCEL_CTRL, ord('T'), AcceleratorIds.CTRL_T),
    (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('S'), AcceleratorIds.CTRL_SHIFT_S)
])