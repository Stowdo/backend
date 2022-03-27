#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

echop 'Cleaning docker from Stowdo containers and images...'

# deleting stowdo containers
for name in stowdo_api_prod stowdo_db_prod stowdo_minio_prod stowdo_proxy_prod \
    stowdo_api_dev stowdo_db_dev stowdo_minio_dev stowdo_proxy_dev
do
    running_container=$(docker ps -f "name=$name" | tail -n +2)
    if [ ! -z "$running_container" ]
    then
        docker stop "$name"
    fi

    container=$(docker ps -a -f "name=$name" | tail -n +2)
    if [ ! -z "$container" ]
    then
        docker rm "$name"
    fi
done

# deleting stowdo images
image=$(docker images -f "reference=redbeandock/stowdo:*" -q)
if [ ! -z "$image" ]
then
    docker rmi "$image"
fi 

echop 'Done'