FROM ubuntu:18.04

ENV TZ 'Europe/Copenhagen'

RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get install -y \
    python3 \
    python3-pip \
    git && \
    apt-get clean

RUN mkdir /home/python_lib && \
    mkdir /home/test

COPY python_lib/ /home/python_lib/
COPY requirements.txt /home
COPY test/ /home/test/
COPY test.py /home
COPY git-mytest.py /home

RUN pip3 install -r /home/requirements.txt && \
    chmod 755 /home/test.py && \
    chmod 755 /home/git-mytest.py

WORKDIR /home