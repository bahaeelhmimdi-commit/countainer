FROM ubuntu:18.04

RUN apt-get update \
 && apt-get install -y \
    git zlib1g-dev openjdk-8-jdk-headless autoconf curl libtool \
    libpq-dev libssl-dev ccache unzip zip python3 rar unrar \
    python3-virtualenv python3-pip pkg-config cmake libffi-dev \
 && pip3 install cython buildozer
RUN mkdir -p /buildozer/ \
 && cd /buildozer/ \
 && git clone https://docker:Ke6M7S98r6NRzHT3nJ7m@gitlab.com/itechia/mediaprest_Group/usine.git \
 && cd usine \
 && unzip cp.zip  \
 && cd cp \
 && unzip nv.zip \
 &&  unrar x -e hamdulah.part1.rar \
 && cd hamdulah \
 && yes | buildozer android debug

VOLUME /buildozer/
VOLUME /p4a/
volume /opt/

WORKDIR /buildozer/

