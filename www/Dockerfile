FROM xeor/base-alpine
MAINTAINER Lars Solberg <lars.solberg@gmail.com>
ENV REFRESHED_AT 2016-12-28

RUN apk update && apk upgrade -U -a \
    && apk add nodejs \
    && npm install --global yarn

COPY root /

WORKDIR /data
COPY data/ /data

