FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends gcc default-jre git

RUN useradd -ms /bin/bash python

ENV MY_PYTHON_PACKAGES=/home/python/app/__pypackages__/3.10
ENV PATH $PATH:${MY_PYTHON_PACKAGES}/bin

ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

RUN pip install pdm

USER python

RUN mkdir /home/python/app

WORKDIR /home/python/app

RUN /bin/bash -c "pdm --pep582 >> ~/.bashrc"