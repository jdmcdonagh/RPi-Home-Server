#!/bin/bash

containers=(
  "pihole-download-backup"
  "pihole-upload-backup"
)

for c in "${containers[@]}"; do
    cd $c
    sudo docker build -t $c .
    docker image tag $c jdmcdonagh/$c:latest
    docker image push jdmcdonagh/$c:latest
    cd ..
done
