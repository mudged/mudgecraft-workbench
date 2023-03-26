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

        -?  --help          Print this message

    For example:

      mc command summon sheep

EOM
}

COMMAND=""

# process arguments
if [[ "$1" -gt 0 ]]; do
    case $1 in

        # commands
        start) shift; mc-start.sh $@;;
        stop) shift; mc-stop.sh $@;;
        reset) shift; mc-reset.sh $@;;
        command) shift; mc-command.sh $@;;
        cmd) shift; mc-command.sh $@;;

        # help
        *) print_usage; exit 0;;

    esac
else
    print_usage;
    exit 0;
fi
