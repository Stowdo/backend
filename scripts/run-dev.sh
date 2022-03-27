#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

set -a
. .env
set +a

if [ ! "$(docker ps -a | grep stowdo_minio_dev)" ]; then
    echop 'Creating minio container...'
    
    docker run \
    -d \
    -h "$MINIO_HOST" \
    --name stowdo_minio_dev \
    -e MINIO_ACCESS_KEY="$MINIO_ACCESS_KEY" \
    -e MINIO_SECRET_KEY="$MINIO_SECRET_KEY" \
    -p "9000:9000" \
    -p "9001:9001" \
    -v "${PWD}/data:/data" \
    bitnami/minio:latest
elif [ ! "$(docker ps | grep stowdo_minio_dev)" ]; then
    echop 'Starting minio...'
    docker start stowdo_minio_dev
fi

if [ $? -eq 0 ]
then
    echop 'Done'
else
    errorp 'Unable to start minio container!'
fi

if [ ! "$(docker ps -a | grep stowdo_db_dev)" ]; then
    echop 'Creating postgresql container...'
    
    docker run \
    -d \
    -h "$STOWDO_DB_HOST" \
    --name stowdo_db_dev \
    -e POSTGRES_DB="$STOWDO_DB_NAME" \
    -e POSTGRES_USER="$STOWDO_DB_USER" \
    -e POSTGRES_PASSWORD="$STOWDO_DB_PASSWORD" \
    -p "${STOWDO_DB_PORT}:5432" \
    -v "${PWD}/scripts/docker:/docker-entrypoint-initdb.d" \
    postgres:14-alpine

    sleep 5
elif [ ! "$(docker ps | grep stowdo_db_dev)" ]; then
    echop 'Starting postgresql...'
    docker start stowdo_db_dev
fi

if [ $? -eq 0 ]
then
    echop 'Done'
else
    errorp 'Unable to start postgresql container!'
fi

echop 'Populating database...'
pipenv run python3 stowdo/manage.py migrate
echop 'Done'

echop 'Running Picdo...'
pipenv run python3 stowdo/manage.py runserver 0.0.0.0:8000
echop 'API stopped'

echop 'Stopping Minio...'
docker stop stowdo_minio_dev
echop 'Done'

echop 'Stopping database...'
docker stop stowdo_db_dev
echop 'Done'