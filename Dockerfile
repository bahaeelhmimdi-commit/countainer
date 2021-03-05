FROM ubuntu:18.04

RUN apt-get update \
 && apt-get install -y \
    git zlib1g-dev openjdk-8-jdk-headless autoconf curl libtool \
    libpq-dev libssl-dev ccache unzip zip python3 rar unrar \
    python3-virtualenv python3-pip pkg-config cmake libffi-dev \
 && pip3 install cython buildozer


VOLUME /buildozer/
VOLUME /p4a/
volume /opt/

WORKDIR /buildozer/

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker
CMD cd /buildozer/
CMD https://docker:Ke6M7S98r6NRzHT3nJ7m@gitlab.com/itechia/mediaprest_Group/usine.git
CMD unzip cp.zip 
CMD cd cp
CMD unzip nv.zip
CMD cd nv
CMD unrar x -e hamdulah.part1.rar
CMD cd hamdulah
CMD buildozer android debug
