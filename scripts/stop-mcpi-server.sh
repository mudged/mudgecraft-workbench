#!/bin/bash

CONTAINER_NAME="minecraft-server"

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to stop the Minecraft Server for the Python mcpi library.

    The following options are supported:

        -?  --help          Print this message

EOM
}

# process arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in

        # help
        *) print_usage; exit 0;;

    esac
done

echo -e "Attempting to stop the Minecraft Server..."
docker inspect ${CONTAINER_NAME} >/dev/null 2>&1 && docker exec ${CONTAINER_NAME} rcon-cli stop || echo -e "The Minecraft Server is not running"