#!/bin/bash

# stop the server if it is running
echo -e "Attempting to stop any existing Minecraft Server..."
docker stop minecraft-server
docker rm minecraft-server

# ensure the mounted minecraft-server directory is created and populated
echo -e "Copying Minecraft Plugins and Mods..."
mkdir -p ${MINECRAFT_SERVER_DATA_DIR}/plugins ${MINECRAFT_SERVER_DATA_DIR}/mods
cp -nvr /minecraft/plugins/* ${MINECRAFT_SERVER_DATA_DIR}/plugins
cp -nvr /minecraft/mods/* ${MINECRAFT_SERVER_DATA_DIR}/mods

# start the server
echo -e "Starting Minecraft Server..."
docker run --rm --detach \
    --name minecraft-server \
    -p 25565:25565 \
    -p 4711:4711 \
    -p 25575:25575 \
    -v mudgecraft-minecraft-server-data:/data \
    -e EULA=TRUE \
    -e TYPE=SPIGOT \
    itzg/minecraft-server