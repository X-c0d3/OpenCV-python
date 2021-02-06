#!/usr/bin/env python3

# Author : Watchara Pongsri
# [github/X-c0d3] https://github.com/X-c0d3/
# Web Site: https://wwww.rockdevper.com

from cv2 import cv2
import sys
from configparser import ConfigParser
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
from datetime import datetime
import time
import threading
from lineNotify import sendNotify


SEND_NOTIFY_INTERVAL = 600

configur = ConfigParser()
configur.read('config.ini')


video_camera = VideoCamera()
# App Globals (do not edit)
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = configur.get('appsettings', 'auth_user')
app.config['BASIC_AUTH_PASSWORD'] = configur.get('appsettings', 'auth_pass')
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)
last_epoch = 0


@ app.route('/')
@ basic_auth.required
def index():
    return render_template('index.html')


def gen(camera):
    global last_epoch
    while True:
        image, found_obj = camera.get_frame()
        res, jpeg = cv2.imencode('.jpg', image)
        if found_obj and (time.time() - last_epoch) > SEND_NOTIFY_INTERVAL:
            last_epoch = time.time()
            print("Send Line Notify!")
            sendNotify("Detecting \n Found Object !! \n Please recheck your IP camera  \n Time:" +
                       datetime.now().strftime("%H:%M:%S"), jpeg)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


@ app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configur.get(
        'appsettings', 'server_port'), debug=False)
