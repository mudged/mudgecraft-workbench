# mudgecraft-workbench
A VSCode Workbench for working with Minecraft Python APIs

## Running the Workbench Image

The workbench image needs to have a number of things configured for it to work correctly.

1. The Docker Socket needs to be mounted
2. The Docker Group ID needs to be added
3. The container port 3400 needs to be mapped to the host port 80
4. A local data directory for the server data and user files

The Docker Group Id can be retrived by running the following:

```` bash
DOCKER_GID=$(getent group docker | awk -F: '{print $3}')
````

Create the local data directory

```` bash
HOST_DATA_DIR="$(pwd)/mudgecraft"
mkdir -p ${HOST_DATA_DIR}/minecraft-server ${HOST_DATA_DIR}/workspace
````


You can then run the docker image using a command like...

````bash
docker run --rm --detach \
    --name mudgecraft-workbench \
    -p 80:3400 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ${HOST_DATA_DIR}:/data \
    -e HOST_DATA_DIR="${HOST_DATA_DIR}" \
    --group-add ${DOCKER_GID} \
    ghcr.io/mudged/mudgecraft-workbench:main
````

You can now access the Workbench at http://localhost/?folder=/data/workspace