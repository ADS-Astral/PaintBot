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
# serial = Serial(  # Establish the connection on a specific port
#     port="/dev/ttyACM0",  # Linux: /dev/ttyACM0
#     baudrate=9600,
#     timeout=1)
# serial.close()
# serial.open()

# Configure depth and color streams
pipeline = rs.pipeline()
pipeline2 = rs.pipeline() # 
config = rs.config()
config2 = rs.config()
config.enable_stream(rs.stream.depth, 424, 240, rs.format.z16, 6)
config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 30)
config2.enable_stream(rs.stream.pose)

# Start streaming
profile = pipeline.start(config)
pipeline2.start(config2)

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


def DistanceControl(motorControl, distance, direction):
    while True:
        #print(distance.value)
        if distance.value >= 0.4:
            motorControl.MoveForward()
        elif distance.value <= 0.2:
            motorControl.MoveReverse()
        else:
            if direction == MotorControl.STATE_LEFT:
                motorControl.MoveLeft()
            elif direction == MotorControl.STATE_RIGHT:
                motorControl.MoveRight()
            else:
                motorControl.Stop()
        pass



def main():

    # motorControl = MotorControl(serial)
    distance = Distance()
    # direction = MotorControl.STATE_RIGHT
    # distanceThread = threading.Thread(target=DistanceControl, args=(motorControl, distance, direction))
    # distanceThread.start()

    #sg.theme_previewer()
    sg.theme('DarkPurple5')

    # ---===--- define the window layout --- # creating video feed, button & slider

    #SimpleGUI layout matches typed structure.
    layout = [
        [
            sg.Text('PAINTBOT 9000_B.Y.', size=(20, 1), font='Helvetica 20'),
            sg.Text('Colour scheme for depth feed:', size=(40, 1), font='Helvetica 10'),
            sg.Slider(range=(0,11),default_value=5,size=(20,15),orientation='horizontal',font=('Helvetica', 12),key='sliderTop'),
            sg.Button('Exit', size=(7, 1), font='Helvetica 14'),
        ],
        [
            sg.Image(filename='', key='-image-'),
            # sg.Image(filename='', key='-image2-'),
        ],
        [
            sg.Text('Distance:', size=(8, 1),font='Helvetica 14'),
            sg.Text(size=(8, 1),font='Helvetica 14',key='distance'),
            sg.Text('Received command:',size=(18, 1),font='Helvetica 14'),
            sg.Text(' ',size=(18, 1),font='Helvetica 14',key='arduino_rec'),
        ],
        [
            sg.Text(' ',size=(35, 1),font='Helvetica 14',key='robo_position_x'),
            sg.Text(' ',size=(10, 1),font='Helvetica 14',key='robo_position_y'),
            sg.Text(' ',size=(10, 1),font='Helvetica 14',key='robo_position_z'),
        ],
        [
            sg.Text(' ',size=(35, 1),font='Helvetica 14',key='robo_velocity_x'),
            sg.Text(' ',size=(10, 1),font='Helvetica 14',key='robo_velocity_y'),
            sg.Text(' ',size=(10, 1),font='Helvetica 14',key='robo_velocity_z'),
        ],
        [
            sg.Text(' ',size=(35, 1),font='Helvetica 14',key='robo_acceleration_x'),
            sg.Text(' ',size=(10, 1),font='Helvetica 14',key='robo_acceleration_y'),
            sg.Text(' ',size=(10, 1),font='Helvetica 14',key='robo_acceleration_z'),
        ],
        [
            sg.Text('Depth Range', size=(15, 1), font='Helvetica 20'),
            sg.Text(' ', size=(4, 1), font='Helvetica 20',key='sliderOutput'),
            sg.Text(' m ', size=(8, 1), font='Helvetica 20'),
            sg.Slider(range=(1,15),default_value=7,size=(20,15),orientation='horizontal',font=('Helvetica', 12),key='sliderBottom'),
        ]
    ]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - Paintbot',
                       layout,
                       no_titlebar=False,
                       location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['-image-']
    # image_elem2 = window['-image2-']

    
#-----Depth clipping feature----------
# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)

    captureSize = None
    captureHalfSize = None


    # ---===--- LOOP through video file by frame --- #
    
    while True:

        #Return events for SIMPLEgui
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            # close the already opened video file
            out.release()
            break
        #--REALSENSE-----------
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        poseframes = pipeline2.wait_for_frames()

        # Align the depth frame to color frame - Clipping feature
        depth_frame = align.process(frames)
        # Getting depth and a colour frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue
        
        
        # Convert images to numpy arrays THESE ARE EQUIVALENT TO  VIDEO FEED e.g. VideoCapture(0)
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # get gyro and accel data
        pose = poseframes.get_pose_frame()
        if pose:
            # Print some of the pose data to the terminal
            data = pose.get_pose_data()

            # position_list = str(data.translation).split(',') # position list [x,y,z]
            # velocity_list = str(data.velocity).split(',') # velocity list [x,y,z]
            # acceleration_list = str(data.acceleration).split(',') # acceleration_list [x,y,z]
           
            window['robo_position_x'].update("Position in meters relative to start: x: {}".format(round(float(data.translation.x), 3)))
            window['robo_position_y'].update("y: {}".format(round(float(data.translation.y), 3)))
            window['robo_position_z'].update("z: {}".format(round(float(data.translation.z), 3)))
            window['robo_velocity_x'].update("Velocity in meters/sec: x: {}".format(round(float(data.velocity.x), 3)))
            window['robo_velocity_y'].update("y: {}".format(round(float(data.velocity.y), 3)))
            window['robo_velocity_z'].update("z: {}".format(round(float(data.velocity.z), 3)))
            window['robo_acceleration_x'].update("Acceleration in meters/sec^2: x: {}".format(round(float(data.acceleration.x), 3)))
            window['robo_acceleration_y'].update("y: {}".format(round(float(data.acceleration.y), 3)))
            window['robo_acceleration_z'].update("z: {}".format(round(float(data.acceleration.z), 3)))
            print("Frame #{}".format(pose.frame_number))
            print("Position: {}".format(data.translation))
            print("Velocity: {}".format(data.velocity))
            print("Acceleration: {}\n".format(data.acceleration))
        

        #Adds text to both video feeds
        font = cv2.FONT_HERSHEY_SIMPLEX
        time_string = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        cv2.putText(color_image,str(time_string),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(color_image,str('Front Cam'),(10,450), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(depth_image,str(time_string),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
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

        if captureSize is None:
            captureSize = bg_removed_colormap.shape[:2]
            captureHalfSize = (int(captureSize[1] / 2), int(captureSize[0] / 2))

        # Stack both images horizontally
        images = np.hstack((color_image, bg_removed_colormap))

        # Collects depth data and prints it in float format
        depth = depth_image[captureHalfSize[1], captureHalfSize[0]].astype(float)
        distance.value = round(depth * depth_scale, 2)            # rounding to 2 sig figs
        
        #Update GUI with distance
        window['distance'].update(distance.value)

        # serial.write(str.encode(chr(48)))  # Convert the decimal number to ASCII then send it to the Arduino
        

        # Collecting indervidual frames converting to an image and updating GUI
        frame = cv2.imencode('.png', images)

        scale_percent = 20
        # width = int(frame1.shape[1] * scale_percent / 100)
        # height = int(frame1.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # small_video = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        imgbytes = frame[1].tobytes()  # create image type
        # imagebytes2 = small_video[1].tobytes
        image_elem.update(data=imgbytes) # Update window in widget
        # image_elem2.update(data=imgbytes2)

        # Sending data to arduino and printing the recieved data from arduino
         
        # 48 = ASCII(0), commands range: 48-56 -> ASCII (0-8)
        # ser.write(str.encode(chr(arduino_command))) # Convert the decimal number to ASCII then send it to the Arduino
       
        # Update GUI with received arduino command
        # window['arduino_rec'].update(serial.readline())
        # Refreshes GUI interface
        window.Refresh()

main() # Run main class
