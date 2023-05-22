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
import numpy as np

from utils_display import DisplayHand, DisplayBody, DisplayHolistic
from utils_mediapipe import MediaPipeHand, MediaPipeBody, MediaPipeHolistic


def extract_pose(input_file,output_file):
    # Read from .mp4 file
    # 输入视频的地址
    cap = cv2.VideoCapture(input_file)

    # Read in sample image to estimate camera intrinsic
    ret, img = cap.read(0)
    # img = cv2.resize(img, None, fx=0.5, fy=0.5)
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

    pipe = MediaPipeBody(static_image_mode=False, model_complexity=1, intrin=intrin)
    disp = DisplayBody(draw3d=True, draw_camera=True, intrin=intrin)

    # log = True
    # count = 0
    # cap.set(cv2.CAP_PROP_POS_FRAMES, 900)

    f = open(output_file, 'w')
    frame=0
    #prev_time = time.time()


    while cap.isOpened():
        ret, img = cap.read()
        frame += 1
        if not ret:
            # cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop back
            # ret, img = cap.read()
            break

        # Write the frame to the video file
        #out.write(img)

        # Read audio data from stream
        #audio_data = stream.read(CHUNK)
        #f1.writeframes(audio_data)

        # # Write audio data to file
        # with open(WAVE_OUTPUT_FILENAME, 'ab') as f1:
        #     f1.write(audio_data)

        # Flip image for 3rd person view
        img = cv2.flip(img, 1)
        # img = cv2.resize(img, None, fx=0.5, fy=0.5)

        # To improve performance, optionally mark image as not writeable to pass by reference
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

        # if log:
        #     img = (np.asarray(disp.vis.capture_screen_float_buffer())*255).astype(np.uint8)
        #     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #     cv2.imwrite('../data/image/'+str(count).zfill(2)+'.png', img)
        #     count += 1

        key = cv2.waitKey(1)
        if key==27:
            break
        if key==ord('r'): # Press 'r' to reset camera view
            disp.camera.reset_view()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if key==32: # Press spacebar to start logging images
        #     log = not log
        #     print('Log', log)

    pipe.pipe.close()
    f.close()
    cap.release()
    #out.release()
    cv2.destroyAllWindows()
    return output_file


if __name__ == '__main__':
    extract_pose('D:\mediapipe_3d\google-mediapipe-main\data\manoftheyear.mp4', 'D:\mediapipe_3d\google-mediapipe-main\out\manoftheyear.txt')