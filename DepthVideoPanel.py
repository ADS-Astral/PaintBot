import wx
import cv2 as cv
import numpy as np
import pyrealsense2 as rs
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
        frames = self.depth_info.GetFrames()

        # Get gyro and accel data
        # motion_data = frames.as_motion_frame().get_motion_data()
        # print(motion_data)
        # print(np.array([motion_data.x, motion_data.y, motion_data.z]))

        # Get distance to object in center of camera feed
        depth_sensor = self.depth_info.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        # Coordinates for the point on the video stream to detect distance
        depth = depth_image[int(self.height / 2), int(self.width / 2)].astype(float)
        distance = depth * depth_scale

        print("Distance (m):  {:.2f}".format(distance))
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=self.distance), colormap=self.colormap)
        buffer = cv.cvtColor(depth_colormap, cv.COLOR_BGR2RGB)
        return buffer

        pass

    pass  # DepthVideoPanel
