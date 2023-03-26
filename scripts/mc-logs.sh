#!/bin/bash

# Local common
. mc-common.sh

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to show the logs of the Minecraft Server.

    The following options are supported:

        -f  --follow        Follow the logs
        -?  --help          Print this message

EOM
}

ARGS=""

# process arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in

        --follow|-f) shift; ARGS="${ARGS} --follow";;

        # help
        *) print_usage; exit 0;;

    esac
done

# show logs
docker logs ${ARGS} ${MC_CONTAINER_NAME}