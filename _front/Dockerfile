FROM xeor/base-alpine
MAINTAINER Lars Solberg <lars.solberg@gmail.com>
ENV REFRESHED_AT 2016-09-29

EXPOSE 8080

COPY root /

RUN apk update && apk add nginx
