# mudgecraft-workbench

A VSCode Workbench for working with Minecraft Python APIs

## Purpose

This project was started as a way to help me teach my kids how to program in Python with Minecraft. It uses a browser accessible Open VSCode Server preconfigured with the tools they need including scripts to start a Minecraft Server. 

It's is desgined to run on a RaspberryPi 4B with 8Gb of RAM with Ubuntu Server and the Docker Engine installed. 

This way my kids can access the workbench via a browser from their laptop, and they only have to install Minecraft Java Edition locally.


## Before Running the Workbench

You must have docker installed and have a user that is a member of the docker group.


### Installing Docker on Windows

On Windows you can install Docker Desktop from https://www.docker.com/products/docker-desktop/. As part of the installation it will enable Windows Sub System for Linux (or WSL). Once Docker Desktop is installed you can create a new WSL Ubuntu distribution using the following commands in a command prompt.

````
wsl --update
wsl --install Ubuntu --no-launch
wsl --set-default Ubuntu
````

Then open Docker Desktop and go to `Settings > Resources > WSL Integration`. Select the new `Ubuntu` distrobution, and `Apply and Restart`.

When you run `wsl` from the command prompt, you will enter into the Ubunto distribution will access to docker. You can test this by running the following.

```` bash
docker run --rm hello-world
````

You can now run the Workbench install script using the instructions below.



### Installing Docker on Linux

When installing on Linux you can use the Docker Engine (rather than the Docker Desktop). Follow the instructions at https://docs.docker.com/engine/install/ for your Linux distribution.

If installing on a Raspberry Pi 4B, then I recommend using the Ubuntu Server distrobution.

Once installed you need to ensure that your user is a member of the `docker` group. You can check this by running `id` and looking in the groups section.

If you are not a member you need to run the following.

```` bash
sudo groupadd docker
sudo usermod -aG docker ${USER}
````
You'll then need to restart the docker engine service (e.g. `sudo systemctl restart docker` or equivilent for your install). You'll probably also need to restart your terminal session as well.

You can then test that docker is working as expected by running the following.

```` bash
docker run --rm hello-world
````

You can now run the Workbench install script using the instructions below.


### Installing Docker on Mac

I haven't been able to test on a Mac as I don't have one. However from past experience it should be similar to the Linux install if you make use of [Colima](https://github.com/abiosoft/colima).


## Running the Workbench Image

You can install/update the Workbench by running the following command.

```` bash
 curl https://raw.githubusercontent.com/mudged/mudgecraft-workbench/main/install.sh | bash
````

You can now access the Workbench at http://localhost/?folder=/home/steve/workspace

If you are accessing the application from a different machine to where you installed it, then you will need to change `localhost` to the name or ip address of your machine.


## Commands within the Workbench

When you are inside the Workbench you will see a Visual Studios interface. Use the menu on the upper right to select `Terminal > New Terminal`. The terminal should appear at the bottom of the screen. You can use the `mc` command to interact with the Minecraft server. Type `mc` to see a list of commands. And `mc <command> --help` to see the options available for that command.

For example you can start the Minecraft server in a flat creative mode with cheats enabled using the following.

````bash
mc start --cheats --creative --flat
````

Or you can pass commands to a running Minecraft server by using the the `mc command`.

````bash
mc command weather clear
````

To stop the Minecraft server use the followin.

````bash
mc stop
````

And to clear the Minecraft world data use the following.

````bash
mc reset
````

## Accessing the Minecraft Server

The Minecraft server can be access from the Minecraft Java Edition client on port `25565` on the computer it was installed on. If you are running on the same machine, then you can use `localhost:25565`.

Within the Visual Studios workbench, the Minecraft server is always acessible a computer called `minecraft`.

## Working with files in the Workbench

A word of caution, only files created under `/home/steve/workspace` will be saved. Any other files will be lost when the docker container is stopped.

Files are saved in a docker volume called `mudgecraft-workspace-data`.