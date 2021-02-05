FROM ubuntu:18.04
LABEL maintainer="rockdevper@gmail.com"

RUN apt-get update -y && apt-get install -y build-essential cmake \
    libsm6 libxext6 libxrender-dev \
    python3 python3-pip python3-dev python3-opencv

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]