FROM python:3.6-slim

WORKDIR /app
ARG REMOTE_HOST

COPY ./cfg /app
COPY ./src /app/src

# RUN pip install parallel-ssh
RUN pip install paramiko
RUN pip install --force-reinstall pip==9.0.3

RUN mkdir python_packages
RUN pip download -r requirements.txt -d '/app/python_packages'
RUN tar cvfz python_packages.tgz python_packages

RUN apt-get update
RUN apt-get -y install sshpass

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan -H $REMOTE_HOST > /root/.ssh/known_hosts