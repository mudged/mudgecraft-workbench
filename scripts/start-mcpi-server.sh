#!/bin/bash

CONTAINER_NAME="minecraft-server"
DIFFICULTY="peaceful"
LEVEL_TYPE="normal"
MODE="creative"

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to (re)start the Minecraft Server for the Python mcpi library.

    The following options are supported:

        -?  --help          Print this message
        --easy              Set the difficulty to easy
        --normal            Set the difficulty to normal
        --hard              Set the difficulty to hard
        --peaceful          Set the difficulty to peaceful (default)
        --flat              Set the Level Type to flat
        --creative          Set the mode to crreative
        --survival          Set the mode to survival

    For example..

        This command will create a flat, peaceful creative world
        start-mcpi-server.sh --flat --peaceful --creative

EOM
}

# process arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in

        # Difficulty
        --easy) shift; DIFFICULTY="easy";;
        --normal) shift; DIFFICULTY="normal";;
        --hard) shift; DIFFICULTY="hard";;
        --peaceful) shift; DIFFICULTY="peaceful";;

        # Level Type
        --flat) shift; LEVEL_TYPE="flat";;

        # Mode
        --creative) shift; MODE="creative";;
        --survival) shift; MODE="survival";;

        *) print_usage; break;;

    esac
done

# stop the server if it is running
echo -e "Attempting to stop any existing Minecraft Server..."
docker inspect ${CONTAINER_NAME} >/dev/null 2>&1 && docker stop ${CONTAINER_NAME} || echo -e "The Minecraft Server is not running"
docker inspect ${CONTAINER_NAME} >/dev/null 2>&1 && docker rm ${CONTAINER_NAME} || echo -e "The Minecraft Server does not exist"

# ensure the mounted minecraft-server directory is created and populated
echo -e "Copying Minecraft Plugins and Mods..."
mkdir -p ${MINECRAFT_SERVER_DATA_DIR}/plugins ${MINECRAFT_SERVER_DATA_DIR}/mods
cp -nvr /minecraft/plugins/* ${MINECRAFT_SERVER_DATA_DIR}/plugins
cp -nvr /minecraft/mods/* ${MINECRAFT_SERVER_DATA_DIR}/mods

# start the server
echo -e "Starting Minecraft Server..."
docker run --rm --detach \
    --name ${CONTAINER_NAME} \
    -p 25565:25565 \
    -p 4711:4711 \
    -p 25575:25575 \
    -v mudgecraft-minecraft-server-data:/data \
    -e SERVER_NAME=Mudgecraft \
    -e EULA=TRUE \
    -e TYPE=SPIGOT \
    -e MOTD="Mudgecarft Spigot Minecraft Server" \
    -e DIFFICULTY="${DIFFICULTY}" \
    -e LEVEL_TYPE=${LEVEL_TYPE} \
    -e MAX_PLAYERS=10 \
    -e MAX_WORLD_SIZE=1000 \
    -e GENERATE_STRUCTURES=true \
    -e SPAWN_ANIMALS=true \
    -e SPAWN_MONSTERS=false \
    -e SPAWN_NPCS=false \
    -e SEED="1785852800490497919" \
    -e MODE=${MODE} \
    -e PVP=false \
    -e ALLOW_CHEATS=true \
    -e ALLOW_FLIGHT=TRUE \
    itzg/minecraft-server

# wait for the server to start
echo -e "Waiting for Minecraft Server to Start. This may take a few minutes...
CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${CONTAINER_NAME} 2> /dev/null | grep "running")
while [[ "${CONTAINER_STATUS}" != "\"running\"" ]]; do
    sleep 2
    CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${CONTAINER_NAME} 2> /dev/null | grep "running")
done
