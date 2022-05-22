FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends gcc default-jre git wget curl zsh fonts-powerline make

RUN useradd -ms /bin/bash python

ENV ROOT_PACKAGES=/home/python/app/__pypackages__/3.10
#ENV CORE_PACKAGES=/home/python/app/src/__core/__pypackages__/3.10
#ENV DJANGO_PACKAGES=/home/python/app/src/django_app/__pypackages__/3.10
#ENV PATH $PATH:${ROOT_PACKAGES}/bin:${CORE_PACKAGES}/bin:${DJANGO_PACKAGES}/bin
ENV PATH $PATH:${ROOT_PACKAGES}/bin

ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src/__core:/home/python/app/src/django_app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

RUN pip install pdm

USER python

RUN mkdir /home/python/app

WORKDIR /home/python/app

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p git-flow \
    -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -a 'export TERM=xterm-256color'

RUN echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc && \
    echo 'eval "$(pdm --pep582)"' >> ~/.bashrc && \
    echo 'eval "$(pdm --pep582)"' >> ~/.zshrc && \
    echo 'HISTFILE=/home/python/zsh/.zsh_history' >> ~/.zshrc
