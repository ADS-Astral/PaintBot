
import wx
import cv2 as cv

class VideoPanel(wx.Panel):
    capture = None
    bitmap = None
    timer = None

    def __init__(self, parent, deviceId=0, fps=15):
        wx.Panel.__init__(self, parent)

        self.capture = cv.VideoCapture(deviceId)
        result, frame = self.capture.read()

        height, width = frame.shape[:2]
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        self.bitmap = wx.BitmapFromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000 / fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)

    def NextFrame(self, event):
        result, frame = self.capture.read()
        if result:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            self.bitmap.CopyFromBuffer(frame)
            self.Refresh()
