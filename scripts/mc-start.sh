#!/bin/bash

# Local common
. mc-common.sh

DIFFICULTY="peaceful"
LEVEL_TYPE="minecraft:normal"
MODE="creative"
STRUCTURES="false"
ANIMALS="false"
MOSTERS="false"
NPCS="false"
CHEATS="false"
FLIGHT="false"
PVP="false"
SEED=
WORLD="basic"
ADDITIONAL_SPIGET_RESOURCES="1997,8846"  # adds the morph plugin

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to (re)start the Minecraft Server.

    The following options are supported:

        --easy              Set the difficulty to easy
        --normal            Set the difficulty to normal
        --hard              Set the difficulty to hard
        --peaceful          Set the difficulty to peaceful (default)

        --flat              Set the Level Type to flat

        --creative          Set the mode to crreative (default)
        --survival          Set the mode to survival

        --animals           Allow animals to spawn
        --monsters          Allow monsters to spawn
        --villagers         Allow Villagers to spawn
        --structures        Generate structures

        --cheats            Allow cheats
        --flight            Allow flight
        --pvp               Allow Players to hurt each other

        --seed              The seed used to create the world

        -?  --help          Print this message

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
        --flat) shift; LEVEL_TYPE="minecraft:flat";;

        # Mode
        --creative) shift; MODE="creative";;
        --survival) shift; MODE="survival";;

        # Spawning
        --animals) shift; ANIMALS="true";;
        --monsters) shift; MONSTERS="true";;
        --villagers) shift; NPCS="true";;
        --structures) shift; STRUCTURES="true";;

        # Cheats
        --cheats) shift; CHEATS="true";;
        --flight) shift; FLIGHT="true";;

        # Seed
        --seed=*) SEED="${1#*=}"; shift;;
        --seed) shift; SEED="${1}"; shift;;

        *) print_usage; exit 0;;

    esac
done

# stop the server if it is running
mc-stop.sh

# ensure the mounted minecraft-server directory is created and populated
# _log_message "Copying Minecraft Plugins and Mods..."
# mkdir -p ${MINECRAFT_SERVER_DATA_DIR}/plugins ${MINECRAFT_SERVER_DATA_DIR}/mods
# cp -nvr /minecraft/plugins/* ${MINECRAFT_SERVER_DATA_DIR}/plugins
# cp -nvr /minecraft/mods/* ${MINECRAFT_SERVER_DATA_DIR}/mods

# check the world exists before using it
if [[ ! -d "/data/minecraft-worlds/${WORLD}" ]]; then
    _log_message "The World '${WORLD}' doesn't exist in /data/minecraft-worlds. Ignoring"
    WORLD=""
fi

# start the server
_log_message "Starting Minecraft Server..."
docker run --rm --detach \
    --name ${MC_CONTAINER_NAME} \
    --network ${NETWORK_NAME} \
    --hostname "minecraft" \
    -p 25565:25565 \
    -p 4711:4711 \
    -p 25575:25575 \
    -v mudgecraft-minecraft-server-data:/data \
    -v mudgecraft-minecraft-world-data:/worlds:ro \
    -e SERVER_NAME=Mudgecraft \
    -e EULA=TRUE \
    -e TYPE=SPIGOT \
    -e SPIGET_RESOURCES=22724,${ADDITIONAL_SPIGET_RESOURCES} \
    -e MOTD="Mudgecarft Spigot Minecraft Server" \
    -e DIFFICULTY=${DIFFICULTY} \
    -e LEVEL_TYPE=${LEVEL_TYPE} \
    -e LEVEL_NAME="Mudgecraft" \
    -e MAX_PLAYERS=10 \
    -e MAX_WORLD_SIZE=1000 \
    -e GENERATE_STRUCTURES=${STRUCTURES} \
    -e SPAWN_ANIMALS=${ANIMALS} \
    -e SPAWN_MONSTERS=${MOSTERS} \
    -e SPAWN_NPCS=${NPCS} \
    -e SEED=${SEED} \
    -e MODE=${MODE} \
    -e PVP=${PVP} \
    -e ALLOW_CHEATS=${CHEATS} \
    -e ALLOW_FLIGHT=${FLIGHT} \
    -e FORCE_WORLD_COPY=true \
    -e WORLD=${WORLD} \
    itzg/minecraft-server > /dev/null

# wait for the server to start
_log_message "Waiting for Minecraft Server to Start."
CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${MC_CONTAINER_NAME} 2> /dev/null | grep "running")
while [[ "${CONTAINER_STATUS}" != "\"running\"" ]]; do
    sleep 2
    CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${MC_CONTAINER_NAME} 2> /dev/null | grep "running")
done
_log_message "Minecraft Server to Started. Waiting for it to become ready. This may take a few minutes..."
CONTAINER_STATUS=$(docker inspect -f='{{json .State.Health.Status}}' ${MC_CONTAINER_NAME} 2> /dev/null | grep "healthy")
while [[ "${CONTAINER_STATUS}" != "\"healthy\"" ]]; do
    sleep 2
    CONTAINER_STATUS=$(docker inspect -f='{{json .State.Status}}' ${MC_CONTAINER_NAME} 2> /dev/null | grep "running")
    if [[ "${CONTAINER_STATUS}" != "\"running\"" ]]; then
        _log_message "Minecraft Server failed to become ready."
        exit 1
    fi
    CONTAINER_STATUS=$(docker inspect -f='{{json .State.Health.Status}}' ${MC_CONTAINER_NAME} 2> /dev/null | grep "healthy")
done

_log_message "Minecraft Server is Ready"