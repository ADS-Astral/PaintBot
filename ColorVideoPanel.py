import cv2 as cv
from VideoPanel import VideoPanel


class ColorVideoPanel(VideoPanel):

    capture = None

    def __init__(self, parent, capture):
        self.capture = capture
        VideoPanel.__init__(self, parent)
        pass

    def GetDataBuffer(self):
        result = True
        buffer = self.capture
        if result:
            buffer = cv.cvtColor(self.capture, cv.COLOR_BGR2RGB)
            return buffer
        else:
            return None  # todo: should be an error
        pass

    pass  # ColorVideoPanel
