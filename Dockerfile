FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y pkg-config
RUN apt-get install -y \
    libavformat-dev libavcodec-dev libavdevice-dev \
    libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
RUN apt-get install -y python3-pip
# RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]
CMD [ "application.py" ]
# EXPOSE 5000
