#!/usr/bin/env python3

# Author : Watchara Pongsri
# [github/X-c0d3] https://github.com/X-c0d3/
# Web Site: https://wwww.rockdevper.com

from cv2 import cv2
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from lineNotify import sendNotify
from threading import Thread

configur = ConfigParser()
configur.read('config.ini')

fullbody_recognition = cv2.CascadeClassifier(
    'models/fullbody_recognition_model.xml')

upperbody = cv2.CascadeClassifier(
    'models/haarcascade_upperbody.xml')


facial_recognition = cv2.CascadeClassifier(
    'models/facial_recognition_model.xml')

eye = cv2.CascadeClassifier(
    'models/haarcascade_eye.xml')

# percent of original size
scale_percent = configur.getint('appsettings', 'scale_percent')


class VideoCamera(object):
    def __init__(self, source=0):

        if (configur.getint('appsettings', 'vdo_mode') == 1):
            # IP Camera
            self.capture = cv2.VideoCapture('{}://{}:{}@{}:{}/tcp/av0_0'.format(
                configur.get('ipcamera', 'protocol'),
                configur.get('ipcamera', 'user'),
                configur.get('ipcamera', 'pass'),
                configur.get('ipcamera', 'ipaddress'),
                configur.getint('ipcamera', 'port')))
            # IP Camera require run with thread
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = True
            self.thread.start()
        elif(configur.getint('appsettings', 'vdo_mode') == 2):
            # Read stream from vdo file
            self.capture = cv2.VideoCapture('./vdo-test.mp4')
        else:
            # Build-in Webcam
            self.capture = cv2.VideoCapture(0)

        # W, H = 1920, 1080
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
        # self.capture.set(cv2.CAP_PROP_FOURCC,
        #                  cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # must set FPS ..25 is max..if i try to set 26 or higher it runs slow. ...this runs 30 fps for me If you not set FPS...it runs slow too
        self.capture.set(cv2.CAP_PROP_FPS, 25)

        self.status = False
        self.frame = None

    def __del__(self):
        # releasing camera
        # self.capture.stop()
        self.capture.release()

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def get_frame(self):
        if (configur.getint('appsettings', 'vdo_mode') != 1):
            self.status, self.frame = self.capture.read()

        if self.status:
            found_objects = False
            vdo = self.frame

            width = int(vdo.shape[1] * scale_percent / 100)
            height = int(vdo.shape[0] * scale_percent / 100)
            dim = (width, height)

            # Resize image
            vdo = cv2.resize(vdo, dim, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(vdo, cv2.COLOR_BGR2GRAY)

            # fullbody = fullbody_recognition.detectMultiScale(
            #     gray,
            #     scaleFactor=1.1,
            #     # scaleFactor=1.2,
            #     # scaleFactor=1.05,
            #     minNeighbors=5,
            #     minSize=(30, 30),
            #     flags=cv2.CASCADE_SCALE_IMAGE
            # )

            humans = upperbody.detectMultiScale(
                gray,
                scaleFactor=1.1,
                # scaleFactor=1.2,
                # scaleFactor=1.05,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            faces = facial_recognition.detectMultiScale(
                gray,
                scaleFactor=1.1,
                # scaleFactor=1.2,
                # scaleFactor=1.05,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            totalPerson = 1
            for (x, y, w, h) in humans:
                # Draw a rectangle around the humans
                cv2.rectangle(vdo, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(vdo, 'person', (x, y-10),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 2)
                totalPerson += 1

            totalFace = 1
            for (fx, fy, fw, fh) in faces:
                # Draw a rectangle around the faces
                cv2.rectangle(vdo, (fx, fy), (fx+fw, fy+fh), (0, 0, 255), 2)
                cv2.putText(vdo, 'face', (fx, fy-10),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
                totalFace += 1
                roi_gray = gray[fy:fy+fh, fx:fx+fw]
                roi_color = vdo[fy:fy+fh, fx:fx+fw]
                # for eye detecting
                eyes = eye.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey),
                                  (ex+ew, ey+eh), (0, 255, 0), 2)
                    cv2.putText(roi_color, 'eye', (ex, ey-10),
                                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)

            # for (ax, ay, aw, ah) in fullbody:
            #     # Draw a rectangle around the body
            #     cv2.rectangle(vdo, (ax, ay),
            #                   (ax + aw, ay + ah), (0, 255, 0), 2)
            #     cv2.putText(vdo, 'full body', (ax, ay-10),
            #                 cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)

            cv2.putText(vdo, 'Status : Detecting ', (40, 40),
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(vdo, f'Total Persons : {totalPerson-1}, Face: {totalFace-1}',
                        (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

            if len(humans) > 0:
                found_objects = True
                print("Humans Detected " + str(totalPerson) +
                      "  Object !! - " + datetime.now().strftime("%H:%M:%S"))

            if len(faces) > 0:
                found_objects = True
                print("Faces Detected " + str(totalFace) +
                      "  Object !! - " + datetime.now().strftime("%H:%M:%S"))

            return (vdo, found_objects)

        return (None, False)
