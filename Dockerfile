FROM ubuntu:18.04

RUN apt update -y && apt-get -y dist-upgrade
RUN apt install -y software-properties-common
 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3.9-distutils
RUN apt-get install -y python3-pip wget

RUN wget https://downloads.mender.io/mender-artifact/3.7.1/linux/mender-artifact

RUN chmod +x mender-artifact
RUN cp mender-artifact /usr/local/bin/

COPY uploader /uploader
COPY requirements.txt /requirements.txt
RUN python3.9 -m pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]