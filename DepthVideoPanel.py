import cv2 as cv
import numpy as np
from VideoPanel import VideoPanel


class DepthVideoPanel(VideoPanel):

    depth_info = None
    distance = 0.08
    colormap = cv.COLORMAP_BONE

    def __init__(self, parent, depth_info):
        self.depth_info = depth_info
        VideoPanel.__init__(self, parent)
        pass

    def GetDataBuffer(self):
        # Start streaming
        # frames = self.depth_info
        # depth_frame = frames.get_depth_frame()
        # depth_image = np.asanyarray(depth_frame.get_data())
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(self.depth_info, alpha=self.distance), colormap=self.colormap)
        buffer = cv.cvtColor(depth_colormap, cv.COLOR_BGR2RGB)
        return buffer
        pass

    pass  # DepthVideoPanel
