#!/bin/bash

CONTAINER_NAME="minecraft-server"

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to stop and clear the Minecraft Server.

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

# call stop
~/scripts/stop-mcpi-server.sh
echo -e "Attempting to clear the Minecraft World data..."
docker run --rm -v mudgecraft-minecraft-server-data:/data busybox rm -rvf /data/server.properties /data/logs /data/.cache /data/world /data/world_nether /data/world_the_end