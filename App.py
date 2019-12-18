import pyrealsense2 as rs
import wx
import cv2 as cv
import matplotlib
import numpy as np


# class PaintBotFrame(wx.Frame):
#
#     capture = None
#     panel = None
#     staticBitmap = None
#     mainSizer = None
#
#     def __init__(self, *args, **kw):
#         super(PaintBotFrame, self).__init__(*args, **kw)
#
#         self.SetTitle("wxPython Frame")
#         self.SetSize((800, 600))
#
#         self.panel = wx.Panel(self)
#         self.mainSizer = wx.BoxSizer(wx.VERTICAL)
#         #self.staticBitmap = wx.StaticBitmap()
#         button = wx.Button(self, wx.ID_ANY, "VIRUS")
#         button.Bind(wx.EVT_BUTTON, self.DoCamera)
#         #self.mainSizer.Add(self.staticBitmap, 0, wx.ALL, 5)
#         self.mainSizer.Add(button, 0, wx.ALL, 5)
#         self.panel.SetSizer(self.mainSizer)
#
#         ret, frame = self.capture.read()
#
#         frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#
#         self.bmp = wx.BitmapFromBuffer(w, h, frame)
#
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#         self.Bind(wx.EVT_TIMER, self.NextFrame)
#
#     def OnPaint(self, event):
#         dc = wx.BufferedPaintDC(self)
#         dc.DrawBitmap(self.bmp, 0, 0)
#
#     def NextFrame(self, event):
#         ret, frame = self.capture.read()
#         if ret:
#             frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#             self.bmp.CopyFromBuffer(frame)
#             self.Refresh()
#
#     def DoCamera(self, event):
#
#         cam = cv.VideoCapture(0)
#         w = cam.get(cv.CAP_PROP_FRAME_WIDTH)
#         h = cam.get(cv.CAP_PROP_FRAME_HEIGHT)
#         stride = 3 * h * w
#
#         while True:
#             ret_val, img = cam.read()
#             img = cv.flip(img, 1)
#             pixels = img.tostring()
#             assert 1.0 == len(pixels) / stride
#             bmp = wx.Bitmap.FromBuffer(w, h, pixels)
#             #bmp.SaveFile("test.bmp", wx.BITMAP_TYPE_BMP)
#             self.staticBitmap = wx.StaticBitmap()
#             self.staticBitmap.SetBitmap(bmp)
#             self.mainSizer.Add(self.staticBitmap, 0, wx.ALL, 5)
#             self.Update()
#             break
#             # cv2.imshow('my webcam', img)
#             if cv.waitKey(1) == 27:
#                 break
#         # cv2.destroyAllWindows()
#
#     def DoSense(self):
#
#         pipe = rs.pipeline()
#         profile = pipe.start()
#         try:
#             msg = ""
#             for i in range(0, 100):
#                 frames = pipe.wait_for_frames()
#                 for f in frames:
#                     msg += "{} {} {} {}".format(
#                         f.profile.stream_index(),
#                         f.profile.stream_name(),
#                         f.profile.stream_type(),
#                         f.profile.unique_id()) + "\n"
#             label = wx.StaticText(self.panel, label=msg, pos=(100, 50), size=(500, 500))
#         finally:
#             pipe.stop()
#

# if __name__ == '__main__':
#     app = wx.App()
#     frame = PaintBotFrame(None)
#     frame.Show()
#     app.MainLoop()

from DepthVideoPanel import DepthVideoPanel


class PaintBotFrame(wx.Frame):

    depthPanel = None
    colormapHash = []

    def __init__(self, parent, size):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=size, style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        colormapSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Color Map"), wx.VERTICAL)

        self.colormapHash = [
            cv.COLORMAP_AUTUMN,
            cv.COLORMAP_BONE,
#            cv.COLORMAP_CIVIDIS,
            cv.COLORMAP_COOL,
            cv.COLORMAP_HOT,
            cv.COLORMAP_HSV,
#            cv.COLORMAP_INFERNO,
            cv.COLORMAP_JET,
#            cv.COLORMAP_MAGMA,
            cv.COLORMAP_OCEAN,
            cv.COLORMAP_PARULA,
            cv.COLORMAP_PINK,
#            cv.COLORMAP_PLASMA,
            cv.COLORMAP_RAINBOW,
            cv.COLORMAP_SPRING,
            cv.COLORMAP_SUMMER,
#            cv.COLORMAP_TURBO,
#            cv.COLORMAP_TWILIGHT,
#            cv.COLORMAP_TWILIGHT_SHIFTED,
#            cv.COLORMAP_VIRIDIS,
            cv.COLORMAP_WINTER,
        ]

        colormapChoiceValues = [
                u"Autumn",
                u"Bone",
#                u"Cividis",
                u"Cool",
                u"Hot",
                u"Hsv",
#                u"Inferno",
                u"Jet",
#                u"Magma",
                u"Ocean",
                u"Parula",
                u"Pink",
#                u"Plasma",
                u"Rainbow",
                u"Spring",
                u"Summer",
#                u"Turbo",
#                u"Twilight",
#                u"Twilight_shifted",
#                u"Viridis",
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

        videoSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Video"), wx.VERTICAL)

        self.depthPanel = DepthVideoPanel(self, pipeline)
        self.depthPanel.SetMinSize(size)
        videoSizer.Add(self.depthPanel, 1, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(videoSizer, 1, wx.EXPAND, 5)

        distanceSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Distance"), wx.HORIZONTAL)

        self.distanceSlider = wx.Slider(distanceSizer.GetStaticBox(), wx.ID_ANY, 0, 0, 100, wx.DefaultPosition,
                                        wx.DefaultSize, wx.SL_HORIZONTAL)
        distanceSizer.Add(self.distanceSlider, 1, wx.ALL, 5)

        self.distanceText = wx.TextCtrl(distanceSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.Size(50, -1), wx.TE_READONLY)
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
        self.UpdateDistance()
        self.UpdateColormap()

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

    DISTANCE_MULTIPLIER = 300

    def SetDistance(self, value=0.03):
        self.distanceSlider.SetValue(value * self.DISTANCE_MULTIPLIER)


    def UpdateDistance(self):
        distanceValue = self.distanceSlider.GetValue() / self.DISTANCE_MULTIPLIER
        self.depthPanel.distance = distanceValue
        self.distanceText.ChangeValue(str(distanceValue))

    def UpdateColormap(self):
        self.depthPanel.colormap = self.colormapHash[self.colormapChoice.GetCurrentSelection()]



if __name__ == '__main__':

    pipeline = rs.pipeline()
    config = rs.config()
    w = 800
    h = 600
    config.enable_stream(rs.stream.depth, w, h, rs.format.z16, 30)
    #config.enable_stream(rs.stream.color, w, h, rs.format.bgr8, 30)
    pipeline.start(config)

    app = wx.App()
    frame = PaintBotFrame(None, (w, h))
    frame.Fit()
    frame.Show()
    app.MainLoop()

    pipeline.stop()
