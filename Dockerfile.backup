FROM python:3.7

COPY requirements.txt /
COPY python_lib /
COPY test.py /
COPY git-mytest /

RUN pip install -r /requirements.txt
RUN chmod 755 /test.py
RUN chmod 755 /git-mytest

ENV TZ=Europe/Copenhagen 

COPY . /app
WORKDIR /app