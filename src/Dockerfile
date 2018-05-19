# Because each new docker container is actually a new instance of an isolated environment,
# it is not needed to install a virtualenv in the image nor use it within a container.

FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1
ENV APP_DIR=/src

RUN mkdir $APP_DIR

WORKDIR $APP_DIR

ADD . $APP_DIR/

RUN pip install -r requirements.txt
