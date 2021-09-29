FROM nginx:1.21-alpine

EXPOSE 80

# remove default and copy over nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d