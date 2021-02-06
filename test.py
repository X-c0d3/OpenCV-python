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
from camera import VideoCamera

if __name__ == '__main__':
    streamer = VideoCamera()
    last_epoch = 0
    while True:
        frame, found_obj = streamer.get_frame()
        # Display the resulting frame
        if (found_obj and time.time() - last_epoch) > 600:
            last_epoch = time.time()
            ret, jpeg = cv2.imencode('.jpg', frame)
            sendNotify("Detecting \n Found Object !! \n Please recheck your IP camera  \n Time:" +
                       datetime.now().strftime("%H:%M:%S"), jpeg)

        if frame is not None:
            cv2.imshow("Home Security IP Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
