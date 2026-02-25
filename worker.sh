#!/bin/bash

sudo /opt/octopus/tentacle/Tentacle create-instance --instance "Tentacle" --config "/etc/octopus/Tentacle/tentacle-Tentacle.config"
sudo /opt/octopus/tentacle/Tentacle new-certificate --instance "Tentacle" --if-blank
sudo /opt/octopus/tentacle/Tentacle configure --instance "Tentacle" --app "/home/Octopus/Applications" --noListen "True" --reset-trust
sudo /opt/octopus/tentacle/Tentacle register-worker --instance "Tentacle" --server "http://localhost:8083/" --name "Worker" --comms-style "TentacleActive" --server-comms-port "10953" --apiKey "API-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" --space "Scratchpad2" --workerpool "Default Worker Pool"
sudo /opt/octopus/tentacle/Tentacle service --install --start --instance "Tentacle"