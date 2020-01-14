import pyrealsense2 as rs
import wx
import cv2 as cv
import matplotlib
import numpy as np




from ColorVideoPanel import ColorVideoPanel
from DepthInfo import DepthInfo
from DepthVideoPanel import DepthVideoPanel
from MotorControl import MotorControl


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)
class PaintBotFrame(wx.Frame):

    capture = None
    depth_info = None

    colorPanel = None
    depthPanel = None
    colormapHash = []

    def __init__(self, parent, capture, depth_info):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.capture = capture
        self.depth_info = depth_info

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Hashmap for gradient colour schemes. Range produces gradients of colour
        # Choice assigns ID -> Colour HashMap. ID=key.
        colormapSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Color Map"), wx.VERTICAL)

        # Gradient schemes
        self.colormapHash = [
            cv.COLORMAP_AUTUMN,
            cv.COLORMAP_BONE,
            cv.COLORMAP_COOL,
            cv.COLORMAP_HOT,
            cv.COLORMAP_HSV,
            cv.COLORMAP_JET,
            cv.COLORMAP_OCEAN,
            cv.COLORMAP_PARULA,
            cv.COLORMAP_PINK,
            cv.COLORMAP_RAINBOW,
            cv.COLORMAP_SPRING,
            cv.COLORMAP_SUMMER,
            cv.COLORMAP_WINTER,
        ]

        colormapChoiceValues = [
                u"Autumn",
                u"Bone",
                u"Cool",
                u"Hot",
                u"Hsv",
                u"Jet",
                u"Ocean",
                u"Parula",
                u"Pink",
                u"Rainbow",
                u"Spring",
                u"Summer",
                u"Winter",
        ]

        self.colormapChoice = wx.Choice(
            colormapSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            colormapChoiceValues,
            0)
        self.colormapChoice.SetSelection(0)
        colormapSizer.Add(self.colormapChoice, 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(colormapSizer, 0, wx.EXPAND, 5)

        videoSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Video"), wx.HORIZONTAL)

        # Must initilaized first
        self.depthPanel = DepthVideoPanel(self, self.depth_info)
        self.colorPanel = ColorVideoPanel(self, self.capture)

        videoSizer.Add(self.colorPanel, 1, wx.ALL | wx.EXPAND, 5)
        videoSizer.Add(self.depthPanel, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(videoSizer, 1, wx.EXPAND, 5)

        distanceSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Distance"), wx.HORIZONTAL)

        self.distanceSlider = wx.Slider(distanceSizer.GetStaticBox(), wx.ID_ANY, 0, 0, 100, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SL_HORIZONTAL)
        distanceSizer.Add(self.distanceSlider, 1, wx.ALL, 5)

        self.distanceText = wx.TextCtrl(
            distanceSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(50, -1),
            wx.TE_READONLY)
        distanceSizer.Add(self.distanceText, 0, wx.ALL, 5)

        mainSizer.Add(distanceSizer, 0, wx.EXPAND, 5)

        confirmSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.okayButton = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        confirmSizer.Add(self.okayButton, 0, wx.ALL, 5)

        self.cancelButton = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        confirmSizer.Add(self.cancelButton, 0, wx.ALL, 5)

        mainSizer.Add(confirmSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.colormapChoice.Bind(wx.EVT_CHOICE, self.OnChooseColormap)
        self.distanceSlider.Bind(wx.EVT_SCROLL, self.OnScrollDistance)
        self.okayButton.Bind(wx.EVT_BUTTON, self.OnClickOkay)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnClickCancel)

        self.SetDistance(self.depthPanel.distance)
        self.SetColormap(self.depthPanel.colormap)

    def __del__(self):
        pass

    def OnChooseColormap(self, event):
        self.UpdateColormap()

    def OnScrollDistance(self, event):
        self.UpdateDistance()

    def OnClickOkay(self, event):
        self.Close()

    def OnClickCancel(self, event):
        self.Close()

    DISTANCE_MULTIPLIER = 200

    def SetDistance(self, value=0.03):
        self.distanceSlider.SetValue(value * self.DISTANCE_MULTIPLIER)

    def UpdateDistance(self):
        distanceValue = self.distanceSlider.GetValue() / self.DISTANCE_MULTIPLIER
        self.depthPanel.distance = distanceValue
        self.distanceText.ChangeValue(str(distanceValue))

    def SetColormap(self, newColormap):
        self.depthPanel.colormap = newColormap

    def UpdateColormap(self):
        self.depthPanel.colormap = self.colormapHash[self.colormapChoice.GetCurrentSelection()]


if __name__ == '__main__':
    app = wx.App()
    app.MainLoop()
    try:
        while True:
            
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

         # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.03), cv.COLORMAP_JET)

        # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

        # Show images
            cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)
            cv.imshow('RealSense', images)
            cv.waitKey(1)
            frame = PaintBotFrame(None, color_image, depth_image)
            frame.Fit()
            frame.Show()

    finally:

    # Stop streaming
        pipeline.stop()

    #frame = PaintBotFrame(None, color_image, depth_image)
   # frame.Fit()
   # frame.Show()
