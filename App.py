import pyrealsense2 as rs
import wx
import cv2
import matplotlib
import numpy


# cv example
cam = cv2.VideoCapture(0)
while True:
    ret_val, img = cam.read()
    img = cv2.flip(img, 1)
    cv2.imshow('my webcam', img)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()


# wx and rs example
app = wx.App()
window = wx.Frame(None, title="wxPython Frame", size=(800, 600))
panel = wx.Panel(window)

pipe = rs.pipeline()
profile = pipe.start()
try:
    msg = ""
    for i in range(0, 100):
        frames = pipe.wait_for_frames()
        for f in frames:
            msg += "{} {} {} {}".format(
                f.profile.stream_index(),
                f.profile.stream_name(),
                f.profile.stream_type(),
                f.profile.unique_id()) + "\n"
    label = wx.StaticText(panel, label=msg, pos=(100, 50), size=(500, 500))
finally:
    pipe.stop()

window.Show(True)
app.MainLoop()
