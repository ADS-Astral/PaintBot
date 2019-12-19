import wx
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
from VideoPanel import VideoPanel


class DepthVideoPanel(VideoPanel):

    pipeline = None
    config = None
    profile = None
    distance = 0.08
    colormap = cv.COLORMAP_BONE

    def __init__(self, parent, pipeline, config):
        self.pipeline = pipeline
        self.config = config
        self.profile = pipeline.start(config)
        VideoPanel.__init__(self, parent)

        pass

    def __del__(self):
        self.pipeline.stop()
        pass

    def GetDataBuffer(self):
        # Start streaming
        try:
            frames = self.pipeline.wait_for_frames(1000)
        except RuntimeError:
            return None  # todo: error for frame not arriving within 1 sec

        # Get gyro and accel data
        motion_data = frames.as_motion_frame().get_motion_data()
        print(motion_data)
        print(np.array([motion_data.x, motion_data.y, motion_data.z]))

        # Get distance to object in center of camera feed
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        # Coordinates for the point on the video stream to detect distance
        depth = depth_image[int(self.height / 2), int(self.width / 2)].astype(float)
        distance = depth * depth_scale

        print("Distance (m):  {:.2f}".format(distance))
        dst = None
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=self.distance), colormap=self.colormap, dst=dst)
        buffer = cv.cvtColor(depth_colormap, cv.COLOR_BGR2RGB)
        return buffer

        pass

    pass  # DepthVideoPanel


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    panel = DepthVideoPanel(frame, rs.pipeline(), rs.config())
    frame.SetSize((panel.width, panel.height))
    frame.Show()
    app.MainLoop()
