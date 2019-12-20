
import cv2 as cv


class DepthInfo:

    pipeline = None
    config = None
    profile = None

    distance = 0.1
    colormap = cv.COLORMAP_JET

    def __init__(self, pipeline, config):
        self.pipeline = pipeline
        self.config = config
        try:
            self.profile = pipeline.start(config)
        except RuntimeError as error:
            print("Pipeline start error: {}".format(str(error)))
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

    pass  # DepthInfo
