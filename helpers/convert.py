import datetime
import wx


def py_date_to_wx_datetime(date):
    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1]-1, tt[0])
    return wx.DateTime.FromDMY(*dmy)