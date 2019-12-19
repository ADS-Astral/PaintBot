import wx
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
from VideoPanel import VideoPanel


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
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        try:
            frames = self.pipeline.wait_for_frames(1000)
        except RuntimeError:
            return None  # todo: error for frame not arriving within 1 sec
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        depth = depth_image[320,240].astype(float)
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
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    panel = DepthVideoPanel(frame, pipeline)
    frame.SetSize((panel.width, panel.height))
    frame.Show()
    app.MainLoop()

pipeline.stop()
