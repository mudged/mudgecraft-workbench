# mudgecraft-workbench

A VSCode Workbench for working with Minecraft Python APIs

## Purpose

This project was started as a way to help me teach my kids how to program in Python with Minecraft. It uses a browser accessible Open VSCode Server preconfigured with the tools they need including scripts to start a Minecraft Server. 

It's is desgined to run on a RaspberryPi 4B with 8Gb of RAM with Ubuntu Server and the Docker Engine installed. 

This way my kids can access the workbench via a browser from their laptop, and they only have to install Minecraft Java Edition locally.


## Before Running the Workbench

You must have docker installed and have a user that is a member of the docker group.

## Running the Workbench Image

You can install/update the Workbench by running the following command.

```` bash
 curl https://raw.githubusercontent.com/mudged/mudgecraft-workbench/main/install.sh | bash
````

You can now access the Workbench at http://localhost/?folder=/home/steve/workspace