FROM nginx:1.21-alpine

EXPOSE 8080
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME
RUN apt install daphne
RUN daphne -b 0.0.0.0 -p 8080 resistance.asgi:channel_layer