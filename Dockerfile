# syntax=docker/dockerfile:1 
FROM fedora:37 AS build

# Root Level functions that needs to be done in the container 
RUN dnf install -y python3-pip gcc python3-devel util-linux procps-ng

WORKDIR /src 

COPY ./src /src
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt 
# RUN rm -rf /src 

FROM build 

WORKDIR /src 