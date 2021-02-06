FROM python:3-slim
LABEL maintainer="rockdevper@gmail.com"

RUN apt update -y && apt install -y libgl1-mesa-dev libgtk2.0-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

COPY . .
RUN pip3 install opencv-python
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD [ "python3", "./main.py" ]