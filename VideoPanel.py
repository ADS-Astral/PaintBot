import wx


class VideoPanel(wx.Panel):

    width = 0
    height = 0

    # The bitmap widget that contains the video.
    bitmap = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Capture first ever frame for testing and specifying dimensions
        buffer = self.GetDataBuffer()
        if buffer is not None:
            self.height, self.width = buffer.shape[:2]
            self.bitmap = wx.Bitmap.FromBuffer(self.width, self.height, buffer)
        self.timer = wx.Timer(self)  # Create and start a thread for reading frame-after-frame:
        self.timer.Start()  # No need to control the speed of the thread since we want maximum speed.
        self.Bind(wx.EVT_PAINT, self.OnPaint)  # Specify callback for whenever panel paints itself.
        self.Bind(wx.EVT_TIMER, self.NextFrame)  # Specify callback for timer of this panel thread.
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)
        pass

    def NextFrame(self, event):
        """
        This method is the thread for reading frames from video.
        """
        buffer = self.GetDataBuffer()
        if buffer is not None:
            # Update bitmap widget with new image frame:
            self.bitmap.CopyFromBuffer(buffer)
            # Refresh panel to draw image into bitmap:
            self.Refresh()
        pass

    def GetDataBuffer(self):
        """
        Abstract method for getting current frame from video.
        """
        pass

    pass  # VideoPanel
