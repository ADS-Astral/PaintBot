import cv2 as cv
import wx
from VideoPanel import VideoPanel


class ColorVideoPanel(VideoPanel):

    capture = None

    def __init__(self, parent, capture):
        self.capture = capture
        VideoPanel.__init__(self, parent)

        pass

    def GetDataBuffer(self):
        result, buffer = self.capture.read()
        if result:
            buffer = cv.cvtColor(buffer, cv.COLOR_BGR2RGB)
            return buffer
        else:
            return None  # error

        pass

    pass  # ColorVideoPanel


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    panel = ColorVideoPanel(frame, cv.VideoCapture(0))
    frame.SetSize((panel.width, panel.height))
    frame.Show()
    app.MainLoop()
