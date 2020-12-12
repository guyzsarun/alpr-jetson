import os
import cv2
import time
import requests

RPI_URL = 'http://172.28.110.23:8000'

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

def send_picture(frame,lp,delay):
    if frame is not None:
        frame = cv2.resize(frame, (0,0), fx=0.6, fy=0.6)
        cv2.imwrite('temp.jpg',frame)
        url = RPI_URL
        files = {'media': open('temp.jpg', 'rb')}
        values = {'lp':lp}
        try:
            requests.post(url, files=files,data=values,timeout=8)
            print('I: Finish sending request')
        except requests.ConnectionError:
            print("E: Connection Error")
            pass
        time.sleep(delay)


def check_thread_alive(thr):
    thr.join(timeout=0.0)
    return thr.is_alive()

def calculate_vote(arr):
    results=""
    print(arr)
    if arr:
        stats={i:arr.count(i) for i in arr}
        results=max(stats, key=lambda key: stats[key])

    return results,[]
