#!/bin/bash

DOCKER_GID=$(getent group docker | awk -F: '{print $3}')

docker run --rm --detach --pull always \
    --name mudgecraft-workbench \
    -p 80:3400 \
    -v mudgecraft-workspace-data:/data/workspace
    -v mudgecraft-minecraft-server-data:/data/minecraft-server
    -v /var/run/docker.sock:/var/run/docker.sock \
    --group-add ${DOCKER_GID} \
    ghcr.io/mudged/mudgecraft-workbench:main