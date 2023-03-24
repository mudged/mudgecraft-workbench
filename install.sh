#!/bin/bash

CONTAINER_NAME="mudgecraft-workbench"
NETWORK_NAME="mudgecraft"
DOCKER_GID=$(getent group docker | awk -F: '{print $3}')

# stop the server if it is running
echo -e "Attempting to stop any existing Mudgecraft Workbench..."
docker inspect ${CONTAINER_NAME} >/dev/null 2>&1 && docker stop ${CONTAINER_NAME} || echo -e "The Mudgecraft Workbench is not running"
docker inspect ${CONTAINER_NAME} >/dev/null 2>&1 && docker rm ${CONTAINER_NAME} || echo -e "The Mudgecraft Workbench does not exist"

# Create the Docker network
echo -e "Creating the Mudgecraft Network..."
docker network inspect ${NETWORK_NAME} >/dev/null 2>&1 || docker network create ${NETWORK_NAME}

# Get latest
echo -e "Fetching the latest Mudgecraft Workbench..."
docker pull ghcr.io/mudged/mudgecraft-workbench:main

# Start container
echo -e "Starting the Mudgecraft Workbench..."
docker run --rm --detach \
    --name ${CONTAINER_NAME} \
    --network ${NETWORK_NAME} \
    -p 80:3400 \
    -v mudgecraft-workspace-data:/data/workspace \
    -v mudgecraft-minecraft-server-data:/data/minecraft-server \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --group-add ${DOCKER_GID} \
    ghcr.io/mudged/mudgecraft-workbench:main

# wait for the container to be running
echo -e "Waiting for Mudgecraft Workbench to Start.."
CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${CONTAINER_NAME} 2> /dev/null | grep "running")
while [[ "${CONTAINER_STATUS}" != "\"running\"" ]]; do
    sleep 2
    CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${CONTAINER_NAME} 2> /dev/null | grep "running")
done

echo -e "Ready to use at http://localhost?folder=/home/steve/workspace"