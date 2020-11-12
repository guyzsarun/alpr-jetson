import os
import cv2
import time
import requests

os.system('sudo service nvargus-daemon restart')

def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=616,
    framerate=30/1,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def send_picture(frame,delay):
    if frame:
        cv2.imwrite('temp.jpg',frame)
        url = 'http://172.28.253.160:8000'
        files = {'media': open('temp.jpg', 'rb')}
        requests.post(url, files=files)
        time.sleep(delay)

def check_thread_alive(thr):
    thr.join(timeout=0.0)
    return thr.is_alive()
