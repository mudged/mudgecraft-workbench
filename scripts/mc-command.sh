#!/bin/bash

# Local common
. mc-common.sh

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to execute a command on the Minecraft Server console.

    The following options are supported:

        -?  --help          Print this message

    For example:

      mc command summon sheep

EOM
}

COMMAND=""

# process arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in

        # help
        --help|-?) print_usage; exit 0;;

        *) COMMAND="${COMMAND} ${1}" shift;;

    esac
done

_log_message "Running ${COMMAND} on Minecraft Server Console"
docker exec ${MC_CONTAINER_NAME} mc-send-to-console ${COMMAND}