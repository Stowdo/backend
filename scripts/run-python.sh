#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

set -a
. .env
set +a

export STOWDO_DB_HOST='localhost'

if [ ! "$(docker ps -a | grep stowdo_db_2)" ]; then
    echop 'Creating postgresql container...'
    
    docker run \
    -d \
    -h "$STOWDO_DB_HOST" \
    --name stowdo_db_2 \
    -e POSTGRES_DB="$STOWDO_DB_NAME" \
    -e POSTGRES_USER="$STOWDO_DB_USER" \
    -e POSTGRES_PASSWORD="$STOWDO_DB_PASSWORD" \
    -p "${STOWDO_DB_PORT}:5432" \
    -v "${PWD}/scripts/docker:/docker-entrypoint-initdb.d" \
    postgres:14-alpine

    sleep 5
    
    echop 'Done'
elif [ ! "$(docker ps | grep stowdo_db_2)" ]; then
    echop 'Starting postgresql...'
    docker start stowdo_db_2
    echop 'Done'
fi

echop 'Populating database...'
python3 stowdo/manage.py migrate
echop 'Done'

echop 'Running Picdo...'
python3 stowdo/manage.py runserver 0.0.0.0:8000
echop 'Stopped'