import time
import threading
import numpy as np


class DepthInfo:

    width = 0
    height = 0

    pipeline = None
    config = None
    profile = None

    distance = 0.1

    process = None

    def __init__(self, pipeline, config):
        self.pipeline = pipeline
        self.config = config
        try:
            self.profile = pipeline.start(self.config)
        except RuntimeError as error:
            print("Pipeline start error: {}".format(str(error)))
        # self.height, self.width = ??? # todo
        self.process = threading.Thread(target=self.Process, args=(1,))
        self.process.start()
        pass

    def __del__(self):
        try:
            self.pipeline.stop()
        except RuntimeError as error:
            print("Pipeline stop error: {}".format(str(error)))
        pass

    def GetFrames(self):
        try:
            return self.pipeline.wait_for_frames(2000)
        except RuntimeError as error:
            print("Frame retrieval error: {}".format(str(error)))
            return None
        pass

    def Process(self, name):
        time.sleep(0.01)
        frames = self.GetFrames()

        # Get gyro and accel data
        # motion_data = frames.as_motion_frame().get_motion_data()
        # print(motion_data)
        # print(np.array([motion_data.x, motion_data.y, motion_data.z]))

        # Get distance to object in center of camera feed
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        # Coordinates for the point on the video stream to detect distance
        depth = depth_image[int(self.height / 2), int(self.width / 2)].astype(float)
        distance = depth * depth_scale

        print("Distance (m): {:.2f}".format(distance))
        pass

    pass  # DepthInfo
