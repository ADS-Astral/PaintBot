#!/usr/bin/env python
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv2
import io
import pyrealsense2 as rs
import numpy as np


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

def main():
    # uncomment to activate theme viewer
    #sg.theme_previewer()
    
    
    sg.theme('DarkPurple5')

    # ---===--- define the window layout --- # creating video feed, button & slider
    layout = [[sg.Text('PaintBotGUI', size=(15, 1), font='Helvetica 20')],
              [sg.Image(filename='', key='-image-')],
              [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
              [sg.Slider(range=(1,500),default_value=222,size=(120,15),orientation='horizontal',font=('Helvetica', 12))]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - Opencv2 Integration',
                       layout,
                       no_titlebar=False,
                       location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['-image-']
    

    # ---===--- LOOP through video file by frame --- #
    cur_frame = 0
    while True:
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            break
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        

        # Convert images to numpy arrays THESE ARE EQUIVALENT TO  VIDEO FEED e.g. VideoCapture(0)
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        frame = images
        
        

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # create image type
        image_elem.update(data=imgbytes) #Update window in widget

main() # Run main class
