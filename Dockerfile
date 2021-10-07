# importing base image
FROM python:3.9.6-alpine

# create directory for user app
RUN mkdir -p /home/app

# Create the home directory and set home to /web
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set env variables so no writing .pyc or buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copying requirement.txt file to present working directory
COPY requirements.txt ./

# installing dependency in container
RUN apk add -U --no-cache \
    build-base \
    libffi-dev
RUN pip install -r requirements.txt

# copying all the files to present working directory
COPY . .

EXPOSE 8000