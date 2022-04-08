#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

set -a
. .env
set +a

if [ $1 = "dev" ] ;
then
    label="${STOWDO_VERSION}-dev"
else
    label="${STOWDO_VERSION}"
fi

echop 'Building image...'
docker build -t redbeandock/stowdo-backend:"${label}" .
echop 'Done'

if [ $1 != "dev" ] ;
then
    echop 'Pushing image...'
    docker push redbeandock/stowdo-backend:"${label}"
    echop 'Done'
fi