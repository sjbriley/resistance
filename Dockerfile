# importing base image
FROM python:3.9.6-alpine

# create directory for user app
RUN mkdir -p /home/app

# Create the app user, so we don't have to run as root. Give write permissions
RUN addgroup -S app && adduser -S -G app app

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
RUN pip install -r requirements.txt

# copying all the files to present working directory
COPY . .

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

EXPOSE 8000

# change user to app right before running
USER app

# running server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
# CMD ["gunicorn", "portfolio.wsgi:application", "--bind", "0.0.0.0:80"]