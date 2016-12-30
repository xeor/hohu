FROM xeor/base-alpine
MAINTAINER Lars Solberg <lars.solberg@gmail.com>
ENV REFRESHED_AT 2016-12-28

COPY ./data/requirements.txt /data/requirements.txt

RUN set -ex \
    && adduser -D -H django \
    && apk update \
    && apk add nginx python3 libuuid libxml2 libpq postgresql-client \
    && apk add --no-cache --virtual .build-deps \
        postgresql-dev gcc python3-dev musl-dev linux-headers \
    && pip3 install -r /data/requirements.txt \
    && apk del .build-deps \

    # While we wait for http://legacy.python.org/dev/peps/pep-0373/ to point "python" to python3
    && ln -s /usr/bin/python3 /usr/bin/python


COPY root /
COPY data /data

HEALTHCHECK CMD /usr/bin/docker-healthcheck
