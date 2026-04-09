FROM nginx:alpine

ENV APP_ENV=dev

COPY app/ /usr/share/nginx/html/
