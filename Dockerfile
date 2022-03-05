# Pull base image
FROM python:3.7 as py3.7
LABEL MAINTAINER Asif Mohammad Mollah

# install tzdata
RUN apt-get update && apt-get install -y tzdata

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /code/
