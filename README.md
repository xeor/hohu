# HOme-HUb (hohu in short)

This project is created to cover some personal needs when it comes to home automation.
I will try to keep the project pepy, up2date and easy to start, but I can't promise anything (exuses like; everything done in my spare-time and so on...).

## Status

Currently, this repository is just a placeholder and will probably not contain much usable stuff.

## Installation

Use the `docker-compose.yml` file as a starting-point.

## Components

### http - `/_/api/`

The endpoint you can send RESTfull queries to, to trigger events.

### websocket - `/_/ws/`

Websocket endpoint, used by other web resources to get events.
This service runs in the same container as the `api`

### http - `/`

Everything under `/` that does NOT start with `_` is handeled by an `Angular` app in the `www` container. It itself got multiple components.

**/infoscreen/**
Listens via websocket for events sent via rest to the api endpoint. This events are displayed here, with a black backround. Perfect for being displayed on example a laser-projector.

### db

PostgreSQL container for a general database we will use.

### redis

Used for caching.

### mq

RabbitMQ server for message-queueing. Used by celery in the api component.
