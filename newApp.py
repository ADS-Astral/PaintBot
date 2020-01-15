from datetime import datetime
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv2
import io
import pyrealsense2 as rs
import numpy as np
from MotorControl import MotorControl
import threading
from serial import Serial


# Configuring Serial Port
serial = Serial(  # Establish the connection on a specific port
    port="COM10",  # /dev/ttyACM0
    baudrate=9600,
    timeout=1)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 6)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale 
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
# Initial test to check depth sensor
#print("Depth Scale is: " , depth_scale)

# Gradient schemes
depth_color_scheme = [
    cv2.COLORMAP_AUTUMN,
    cv2.COLORMAP_BONE,
    cv2.COLORMAP_COOL,
    cv2.COLORMAP_HOT,
    cv2.COLORMAP_HSV,
    cv2.COLORMAP_JET,
    cv2.COLORMAP_OCEAN,
    cv2.COLORMAP_PARULA,
    cv2.COLORMAP_PINK,
    cv2.COLORMAP_RAINBOW,
    cv2.COLORMAP_SPRING,
    cv2.COLORMAP_SUMMER,
    cv2.COLORMAP_WINTER,
        ]


class Distance:
    value = 0
    pass


def DistanceControl(motorControl, distance):
    while True:
        print(distance.value)
        if distance.value >= 0.4:
            motorControl.MoveForward()
        elif distance.value <= 0.2:
            motorControl.MoveReverse()
        pass


def main():

    distance = Distance()
    motorControl = MotorControl(serial)
    distanceThread = threading.Thread(target=DistanceControl, args=(motorControl, distance))
    distanceThread.start()

    #sg.theme_previewer()
    sg.theme('DarkPurple5')

    # ---===--- define the window layout --- # creating video feed, button & slider

    #SimpleGUI layout matches typed structure.
    layout = [[sg.Text('PAINTBOT 9000', size=(15, 1), font='Helvetica 20'),sg.Text('            Colour scheme for depth feed:', size=(40, 1), font='Helvetica 10'),sg.Slider(range=(0,11),default_value=5,size=(20,15),orientation='horizontal',font=('Helvetica', 12),key='sliderTop'),sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')],
              [sg.Image(filename='', key='-image-'),sg.Image(filename='', key='-image2-')],
              [sg.Text('Distance:', size=(8, 1),font='Helvetica 14'), sg.Text(size=(8, 1),font='Helvetica 14',key='distance'),sg.Text('Received command:',size=(18, 1),font='Helvetica 14'), sg.Text(' ',size=(18, 1),font='Helvetica 14',key='arduino_rec')],
              [],
              [sg.Text('Depth Range', size=(15, 1), font='Helvetica 20'),sg.Text(' ', size=(4, 1), font='Helvetica 20',key='sliderOutput'),sg.Text(' m ', size=(8, 1), font='Helvetica 20'),sg.Slider(range=(1,15),default_value=7,size=(20,15),orientation='horizontal',font=('Helvetica', 12),key='sliderBottom')]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - Paintbot',
                       layout,
                       no_titlebar=False,
                       location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['-image-']
    image_elem2 = window['-image2-']

    
#-----Depth clipping feature----------
# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)


    # ---===--- LOOP through video file by frame --- #
    
    while True:

        #Return events for SIMPLEgui
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            break
        #--REALSENSE-----------
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame - Clipping feature
        depth_frame = align.process(frames)
        #Getting depth and a colour frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        
        # Convert images to numpy arrays THESE ARE EQUIVALENT TO  VIDEO FEED e.g. VideoCapture(0)
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        #Adds text to both video feeds
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(color_image,str(datetime.now()),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(color_image,str('Front Cam'),(10,450), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(depth_image,str(datetime.now()),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(depth_image,str('Depth Cam'),(10,450), font, 1,(255,255,255),2,cv2.LINE_AA)
        
        #Converting slider point to variables & updating GUI
        slider_top_value = values['sliderTop']
        slider_bottom_value = values['sliderBottom']
        window['sliderOutput'].update(slider_bottom_value)

        # We will be removing the background of objects more than
        #  clipping_distance_in_meters meters away
        clipping_distance_in_meters = slider_bottom_value 
        clipping_distance = clipping_distance_in_meters / depth_scale
        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        #depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image > clipping_distance) | (depth_image <= 0), grey_color, depth_image)

        

        # Apply colormap on depth images (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), depth_color_scheme[int(slider_top_value)])
        bg_removed_colormap = cv2.applyColorMap(cv2.convertScaleAbs(bg_removed, alpha=0.03), depth_color_scheme[int(slider_top_value)])

        # Stack both images horizontally
        images = np.hstack((color_image, bg_removed_colormap))

        # Collects depth data and prints it in float format
        depth = depth_image[320,240].astype(float)          # 320,240 is center of screen
        distance.value = round(depth * depth_scale, 2)            # rounding to 2 sig figs
        
        #Update GUI with distance
        window['distance'].update(distance.value)
        

        # Collecting indervidual frames converting to an image and updating GUI
        frame = images
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # create image type
        image_elem.update(data=imgbytes)                     # Update window in widget

        # Update GUI with received arduino command
        window['arduino_rec'].update(serial.readline())
        # Refreshes GUI interface
        window.Refresh()


main()  # Run main class
