#!/usr/bin/env python3
from cv2 import cv2
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from lineNotify import sendNotify

configur = ConfigParser()
configur.read('config.ini')


fullbody_recognition = cv2.CascadeClassifier(
    'models/fullbody_recognition_model.xml')

upperbody = cv2.CascadeClassifier(
    'models/haarcascade_upperbody.xml')


facial_recognition = cv2.CascadeClassifier(
    'models/facial_recognition_model.xml')

# video = cv2.VideoCapture('./vdo3.mp4')
video = cv2.VideoCapture('{}://{}:{}@{}:{}/tcp/av0_0'.format(
    configur.get('ipcamera', 'protocol'),
    configur.get('ipcamera', 'user'),
    configur.get('ipcamera', 'pass'),
    configur.get('ipcamera', 'ipaddress'),
    configur.getint('ipcamera', 'port')))


i = 0
last_epoch = 0
while True:
    # Capture frame-by-frame
    ret, frame = video.read()

    scale_percent = 70  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # Resize image
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
        cv2.rectangle(frame, (ax, ay), (ax + aw, ay + ah), (0, 255, 0), 2)
        cv2.putText(frame, 'full body', (ax, ay-10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 2)

    cv2.putText(frame, 'Status : Detecting ', (40, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f'Total Persons : {totalPerson-1}, Face: {totalFace-1}',
                (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

    # Display the resulting frame
    if len(humans) > 0:
        if (time.time() - last_epoch) > 600:
            last_epoch = time.time()
            ret, jpeg = cv2.imencode('.jpg', frame)
            sendNotify("Detecting \n Found Object !! \n Please recheck your IP camera  \n Time:" +
                       datetime.now().strftime("%H:%M:%S"), jpeg.tobytes())

    cv2.imshow('IP Camera', frame)

    i += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video.release()
cv2.destroyAllWindows()
