FROM ubuntu:18.04

ENV TZ 'Europe/Copenhagen'

RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get install -y \
    python3=3.6.5-3ubuntu1 \
    python3-pip=9.0.1-2.3~ubuntu1 \
    git=1:2.17.1-1ubuntu0.1 && \
    apt-get clean

RUN mkdir /home/python_lib && \
    mkdir /home/test

COPY python_lib/* /home/python_lib/
COPY requirements.txt /home
COPY test/* /home/test/
COPY test.py /home
COPY git-mytest.py /home

RUN pip3 install -r /home/requirements.txt && \
    chmod 755 /home/test.py && \
    chmod 755 /home/git-mytest.py && \
    ls -all /

WORKDIR /home