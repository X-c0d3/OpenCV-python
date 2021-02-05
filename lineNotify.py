#!/usr/local/bin/python3
import requests
from configparser import ConfigParser
configur = ConfigParser()
configur.read('config.ini')

LINE_ACCESS_TOKEN = configur.get('line-notify', 'token')
URL_LINE = configur.get('line-notify', 'url')


def sendNotify(message, img=None):
    file_img = {'imageFile': img}
    msg = ({'message': message})
    LINE_HEADERS = {"Authorization": "Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    r = session.post(URL_LINE, headers=LINE_HEADERS, files=file_img, data=msg)
    print(r.text)
