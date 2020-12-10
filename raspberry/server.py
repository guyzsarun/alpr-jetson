import threading

from dynaconf import settings
import requests
import shutil
import matplotlib.pyplot as plt
from datetime import datetime
import cv2
from flask import Response, Flask, request
from imutils.video import FPS
from imutils.video import WebcamVideoStream

from utils import line_notify

global video_frame
global fps_i
fps_i = None
video_frame = None

global thread_lock
thread_lock = threading.Lock()

TF_SERVING=settings.TF_SERVING_URL

app = Flask(__name__)
@app.route("/" ,methods = ['POST'])
def notify():
    file = request.files['media']
    lp=request.form['lp']
    file.save('tmp.jpg')

    th = threading.Thread(target=post_process,args=(lp,'tmp.jpg'))
    th.start()
    return '200 OK'

@app.route("/steam")
def streamFrames():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

def post_process(lp,img_path):
    if len(lp)==0:
        msg="Open Gate: http://guyzsarun.southeastasia.cloudapp.azure.com:5000/open \nLP : Not detected"
    else:
        msg="Open Gate: http://guyzsarun.southeastasia.cloudapp.azure.com:5000/open \nLP : "+lp
    try:
        r=requests.post(TF_SERVING,files={'media':open(img_path,'rb')})
        if r.status_code==404:
            line_notify(msg,img_path,False)
        else:
            with open('lp.jpg', 'wb') as f:
                f.write(r.content)
            line_notify(msg,'lp.jpg',False)
    except:
        print("Error sending request")
        pass

def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue

            global fps_i
            if fps_i is None:
                fps_i=0

            cv2.rectangle(video_frame,(30,30),(610,450),(0,0,255),2)
            if fps_i:
                cv2.putText(video_frame, "FPS: {:.2f}".format(fps_i), (25, 25) , cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255))

            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encoded_image) + b'\r\n')


def captureFrames():
    global video_frame, thread_lock, fps_i

    # Video capturing from OpenCV
    video_capture = cv2.VideoCapture(0)

    while True :
        ret,frame = video_capture.read()

        if frame is None:
            continue

        with thread_lock:
            fps_i = video_capture.get(cv2.CAP_PROP_FPS)
            video_frame = frame.copy()

        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()

if __name__ == '__main__':
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    process_thread.start()

    app.run("0.0.0.0", port="8000")