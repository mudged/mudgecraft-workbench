#!/bin/bash

# Local common
. mc-common.sh

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to stop the Minecraft Server.

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

# call stop (graceful) if the container exists
_log_message "Attempting to stop the Minecraft Server..."
docker inspect ${MC_CONTAINER_NAME} >/dev/null 2>&1 && docker exec ${MC_CONTAINER_NAME} rcon-cli stop || _log_message "The Minecraft Server does not exist"

# loop until the container is fully stopped
while [[ $(docker ps | grep "${MC_CONTAINER_NAME}") ]]; do
    sleep 1
done

_log_message "Minecraft Server has stopped"
