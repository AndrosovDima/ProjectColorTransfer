FROM python:3.8

RUN mkdir /workdir
WORKDIR /workdir

COPY requirements.txt /workdir
COPY . /workdir

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --upgrade pip -r requirements.txt

EXPOSE 5000
