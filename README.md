![schedule](https://github.com/X-c0d3/OpenCV-python/blob/main/ScreenShot1.png)

## macOS

pip3 install opencv-python
pip3 install -r requirements.txt

## For Linux
apt install python3-opencv libgl1-mesa-dev libgtk2.0-dev
apt install libatlas-base-dev
pip3 install -r requirements.txt

## For docker
docker build -t opencv-demo:v1 .
docker run -d -p 3000:3000 opencv-demo:v1
go to http://localhost:3000

## How to use
- Change config.ini
- Execute file
   python3 ./main.py
  or
   python3 ./test.py
