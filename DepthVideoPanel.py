import wx
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
from VideoPanel import VideoPanel

# x, y coordinates for the point on the video stream to detect distance
X = 320
Y = 240

class DepthVideoPanel(VideoPanel):

    pipeline = None
    distance = 0.08
    colormap = cv.COLORMAP_BONE

    def __init__(self, parent, pipeline):
        self.pipeline = pipeline
        VideoPanel.__init__(self, parent)

        pass

    def GetDataBuffer(self):
        # Start streaming
        frames = self.pipeline.wait_for_frames(1000)

        # get distance to object in center of camera feed
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        try:
            frames = self.pipeline.wait_for_frames(1000)
        except RuntimeError:
            return None  # todo: error for frame not arriving within 1 sec
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        depth = depth_image[Y, X].astype(float)
        distance = depth * depth_scale

        print("Distance (m):  {:.2f}".format(distance))
        dst = None
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=self.distance), colormap=self.colormap, dst=dst)
        buffer = cv.cvtColor(depth_colormap, cv.COLOR_BGR2RGB)
        return buffer

        pass

    pass  # DepthVideoPanel


pipeline = rs.pipeline()
config = rs.config()
profile = pipeline.start(config)

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    panel = DepthVideoPanel(frame, pipeline)
    frame.SetSize((panel.width, panel.height))
    frame.Show()
    app.MainLoop()

pipeline.stop()
