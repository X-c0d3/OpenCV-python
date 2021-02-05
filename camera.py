#!/usr/bin/env python3
from cv2 import cv2
import imutils
import time
from datetime import datetime
from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')

fullbody_recognition = cv2.CascadeClassifier(
    'models/fullbody_recognition_model.xml')

upperbody = cv2.CascadeClassifier(
    'models/haarcascade_upperbody.xml')


facial_recognition = cv2.CascadeClassifier(
    'models/facial_recognition_model.xml')


class VideoCamera(object):

    def __init__(self):
        # self.video = cv2.VideoCapture('./vdo3.mp4')
        self.video = cv2.VideoCapture('{}://{}:{}@{}:{}/tcp/av0_0'.format(
            configur.get('ipcamera', 'protocol'),
            configur.get('ipcamera', 'user'),
            configur.get('ipcamera', 'pass'),
            configur.get('ipcamera', 'ipaddress'),
            configur.getint('ipcamera', 'port')))

    def __del__(self):
        # releasing camera
        # self.video.stop()
        self.video.release()

    def get_frame(self):
        # extracting frames
        found_objects = False
        ret, frame = self.video.read()
        if ret is not None:
            scale_percent = 80  # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)

            # # Resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            fullbody = fullbody_recognition.detectMultiScale(
                gray,
                scaleFactor=1.1,
                # scaleFactor=1.2,
                # scaleFactor=1.05,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            humans = upperbody.detectMultiScale(
                gray,
                scaleFactor=1.1,
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
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, 'person', (x, y-10),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 2)
                totalPerson += 1

            totalFace = 1
            for (ex, ey, ew, eh) in faces:
                # Draw a rectangle around the faces
                cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
                cv2.putText(frame, 'face', (ex, ey-10),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
                totalFace += 1

            for (ax, ay, aw, ah) in fullbody:
                # Draw a rectangle around the body
                cv2.rectangle(frame, (ax, ay),
                              (ax + aw, ay + ah), (0, 255, 0), 2)
                cv2.putText(frame, 'full body', (ax, ay-10),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)

            cv2.putText(frame, 'Status : Detecting ', (40, 40),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f'Total Persons : {totalPerson-1}, Face: {totalFace-1}',
                        (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)

            if len(humans) > 0:
                found_objects = True
                print("Humans Detected " + str(totalPerson) +
                      "  Object !! - " + datetime.now().strftime("%H:%M:%S"))

            if len(faces) > 0:
                found_objects = True
                print("Faces Detected " + str(totalFace) +
                      "  Object !! - " + datetime.now().strftime("%H:%M:%S"))

            ret, jpeg = cv2.imencode('.jpg', frame)
            return (jpeg.tobytes(), found_objects)
