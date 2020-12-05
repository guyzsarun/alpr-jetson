import os
import time

import jetson.inference
import jetson.utils

import cv2
import requests
import threading
import numpy as np
from imutils.video import FPS

from utils import gstreamer_pipeline, check_thread_alive, send_picture, calculate_vote
from alpr import detect_plate,accum_vote


delay=5

cap_width=1920
cap_height=1080

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

def detect(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA).astype(np.float32)
    img = jetson.utils.cudaFromNumpy(img)
    detections = net.Detect(img, 1280, 720)
    img = jetson.utils.cudaToNumpy(img, 1280, 720, 4)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR).astype(np.uint8)
    return img, detections


def get_bbox(detection):
    num=detection.ClassID
    x1,y1,x2,y2=[int(i) for i in detection.ROI]
    return  num,x1,y1,x2,y2

def main():
    cap = cv2.VideoCapture(gstreamer_pipeline(capture_width=cap_width,capture_height=cap_height,flip_method=2), cv2.CAP_GSTREAMER)
    #cap = cv2.VideoCapture('../video-test2.mp4')
    if cap.isOpened():
        window_handle = cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)

        fps_i=None
        detection=0
        empty_frame=0
        arr=[]

        th = threading.Thread(target=send_picture, args=(None,None,delay))
        th.start()

        while cv2.getWindowProperty("frame", 0) >= 0:
            fps=FPS().start()

            ret_val, img = cap.read()

            frame = img.copy()
            img,detections=detect(img)

            #print("# detected : ",len(detections))

            for i in range(len(detections)):
                num,x1,y1,x2,y2=get_bbox(detections[i])

                if num in [3,4,6,8]:
                    detection=detection+1
                    crop = frame[y1:y2,x1:x2]
                    results=detect_plate(crop)
                    #print(results)

                    if results['results']:
                        arr=accum_vote(results['results'],arr)

                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),4)

            if detection>=10:
                detection=0
                if not check_thread_alive(th):
                    results,arr=calculate_vote(arr)
                    th = threading.Thread(target=send_picture, args=(frame,results,delay))
                    th.start()
                    print(results)
                else:
                    pass

            cv2.imshow("frame", img)

            if fps_i is None:
                fps_i=0

            fps.update()
            fps.stop()
            fps_i=fps.fps()

            #print("FPS: {:.2f}".format(fps.fps()))

            keyCode = cv2.waitKey(30) & 0xFF
            if keyCode == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

if __name__ == "__main__":
    main()
