#!/bin/sh

requeriments() {
    clear && apt-get update \
    && apt -y install curl
}

installDocker() {
    clear && curl -fsSL \
    https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm get-docker.sh
}

installCompose() {
    clear && sudo curl -L \
    "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose \
    && sudo chmod +x /usr/local/bin/docker-compose \
    && sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
}

version() {
    requeriments
    installDocker
    installCompose
    clear && docker --version && docker-compose --version
}

version