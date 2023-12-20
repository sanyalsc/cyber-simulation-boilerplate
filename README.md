# Cyber security simulator

This project contains boilerplate code for simulating one or more agents interacting with each other in a network.  You can define actions for each agent in your simulation using shell scripts and launch the entire simulation with a single command.

## Requirements
You will need to create one or more docker containers which will run the code.  A basic docker container appropriate for the DNS spoofing example is provided under runtine/docker.

## Setup

Once you have the code that you want each agent in your simulation to execute, you will have to define a docker compose file that outlines the simulation.

The networks section of the docker compose file contains the networks in your simulation.  MacVlan is used to allow each individual agent to have its own MAC and IP combination to simulate a real machine connected to a network.

The services section contains the definition for each agent in the simulation; the entrypoint is the code that each agent will execute.  See the dns-spoof-example.yaml file for an example.

## Usage

1) Create docker compose file in a new directory under runtime:
    - fill in appropriate IP info for each agent
    - fill in entrypoints and mount location of codebase on the host machine


If your simulation requires access to the outside internet (like the example does), change the ip, gateway, and set the parent of the driver_opts to match the physical interface the host is using to connect to the net.

2) Build the docker with build.sh

3) cd to the directory in "runtime" with the experiment you want to run

4) run 
    $ docker compose up -d

5) If manual interaction is required, you can attach to containers you want to run commands from
    $ docker attach <container name>
