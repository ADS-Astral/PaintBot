import wx


class VideoPanel(wx.Panel):

    fps = 15
    width = 0
    height = 0
    bitmap = None
    timer = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        frame = self.GetDataBuffer()
        self.height, self.width = frame.shape[:2]

        self.bitmap = wx.BitmapFromBuffer(self.width, self.height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000 / self.fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)

        pass

    def NextFrame(self, event):
        frame = self.GetDataBuffer()
        self.bitmap.CopyFromBuffer(frame)
        self.Refresh()

        pass

    def GetDataBuffer(self):

        pass

    pass  # VideoPanel
