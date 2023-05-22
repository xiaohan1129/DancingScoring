###############################################################################
### Simple demo on displaying 3D hand/body skeleton
### Input : Live video of hand/body
### Output: 3D display of hand/body skeleton 
### Usage : python 08_skeleton_3D.py -m hand
###       : python 08_skeleton_3D.py -m body
###       : python 08_skeleton_3D.py -m holistic
###############################################################################

import cv2
import time
import argparse
import numpy as np
import wave

from utils_display import DisplayHand, DisplayBody, DisplayHolistic
from utils_mediapipe import MediaPipeHand, MediaPipeBody, MediaPipeHolistic

# parser = argparse.ArgumentParser()
# parser.add_argument('-m', '--mode', default='body', help=' Select mode: hand / body / holistic')
# args = parser.parse_args()
# mode = args.mode

# Start video capture
# 摄像头分析模式
# By default webcam is index 0
def record(filename = 'output'):
    cap = cv2.VideoCapture(0)
    #audio = cv2.audioio.AudioCapture(0)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
    fps = 30.0 # frames per second

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename + '.mp4', fourcc, fps, (width, height))

    ret, img = cap.read(0)
    img_width  = img.shape[1]
    img_height = img.shape[0]
    intrin = {
        'fx': img_width*0.9, # Approx 0.7w < f < w https://www.learnopencv.com/approximate-focal-length-for-webcams-and-cell-phone-cameras/
        'fy': img_width*0.9,
        'cx': img_width*0.5, # Approx center of image
        'cy': img_height*0.5,
        'width': img_width,
        'height': img_height,
    }


    # Note: As of version 0.8.3 3D joint estimation is only available in full body mode
    pipe = MediaPipeBody(static_image_mode=False, model_complexity=1, intrin=intrin)
    disp = DisplayBody(draw3d=True, draw_camera=True, intrin=intrin)


    f = open(filename +'.txt', 'w')
    frame=0
    prev_time = time.time()


    while cap.isOpened():
        ret, img = cap.read()
        frame += 1
        if not ret:
            break

        # Write the frame to the video file
        out.write(img)

        # Flip image for 3rd person view
        img = cv2.flip(img, 1)

        img.flags.writeable = False

        # Feedforward to extract keypoint
        param = pipe.forward(img)
        joints = param['joint']
        out_jonts=''
        for i in range(joints.shape[0]):
            coor=joints[i]
            out_jonts+='('+str(coor[0])+','+str(coor[1])+','+str(coor[2])+');'
        f.write(str(frame) + ',joints,' + str(out_jonts) + '\n') 

        img.flags.writeable = True
        # Display keypoint
        cv2.imshow('img 2D', disp.draw2d(img, param))
        # Display 3D
        disp.draw3d(param, img)
        disp.vis.update_geometry(None)
        disp.vis.poll_events()
        disp.vis.update_renderer()    


        key = cv2.waitKey(1)
        # if key==27:
        #     break
        # if key==ord('r'): # Press 'r' to reset camera view
        #     disp.camera.reset_view()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    pipe.pipe.close()
    f.close()
    cap.release()
    out.release()
# audio.terminate()
    cv2.destroyAllWindows()
