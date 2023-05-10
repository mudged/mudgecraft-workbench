#!/bin/bash

# Local common
. mc-common.sh

# Print Usage
function print_usage() {

    cat <<-EOM
This script is used to control the Minecraft Server.

    The following options are supported:

        start               Start the Minecraft Server
        stop                Stop the Minecraft Server
        reset               Reset the Minecraft Server
        command             Run a command on the Minecraft Server console
        logs                Show the logs for the Minecraft Server

        -?  --help          Print this message

    For example:

      mc start --create --flat

      mc command time set day

EOM
}

# process arguments
if [[ "${#1}" -gt 0 ]]; then
    case "${1}" in

        # commands
        start) shift; mc-start.sh $@;;
        stop) shift; mc-stop.sh $@;;
        reset) shift; mc-reset.sh $@;;
        command|cmd) shift; mc-command.sh $@;;
        log|logs) shift; mc-logs.sh $@;;

        # help
        *) print_usage; exit 0;;

    esac
else
    print_usage;
    exit 0;
fi
