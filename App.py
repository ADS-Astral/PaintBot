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
#
# if __name__ == '__main__':
#     app = wx.App()
#     frame = PaintBotFrame(None)
#     frame.Show()
#     app.MainLoop()

import VideoPanel

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    panel = VideoPanel(frame)
    frame.Show()
    app.MainLoop()
