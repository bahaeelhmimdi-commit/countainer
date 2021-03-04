FROM ubuntu:18.04

RUN apt-get update \
 && apt-get install -y \
    git zlib1g-dev openjdk-8-jdk-headless autoconf curl libtool \
    libpq-dev libssl-dev ccache unzip zip python3 \
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
CMD mkdir /var/local/temp_for_zip_extract

CMD wget https://itechiaio-my.sharepoint.com/personal/bahae_elhmimdi_i-techia_com/_layouts/15/download.aspx?SourceUrl=%2Fpersonal%2Fbahae%5Felhmimdi%5Fi%2Dtechia%5Fcom%2FDocuments%2Fcp%2Ezip
CMD unzip cp.zip -d /var/local/temp_for_zip_extract

