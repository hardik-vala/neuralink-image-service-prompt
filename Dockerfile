FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /root
COPY . /root

RUN ./setup
RUN pip install pylint
