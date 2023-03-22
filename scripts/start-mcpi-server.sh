#!/bin/bash

# stop the server if it is running
echo -e "Attempting to stop any existing Minecraft Server..."
docker stop minecraft-server
docker rm minecraft-server

# ensure the mounted minecraft-server directory is created and populated
echo -e "Copying Minecraft Plugins and Mods..."
mkdir -p /data/minecraft-server/plugins /data/minecraft-server/mods
cp -r /minecraft/plugins /data/minecraft-server/plugins
cp -r /minecraft/mods /data/minecraft-server/mods

# start the server
echo -e "Starting Minecraft Server..."
docker run --rm --detach \
    --name minecraft-server \
    -p 25565:25565 \
    -p 4711:4711 \
    -p 25575:25575 \
    -v ${HOST_DATA_DIR}/minecraft-server:/data \
    -e EULA=TRUE \
    -e TYPE=SPIGOT \
    itzg/minecraft-server