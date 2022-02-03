#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

set -a
. .env
set +a

echop 'Building image...'
docker build -t redbeandock/stowdo-backend:"${STOWDO_VERSION}" .
echop 'Done'

echop 'Pushing to Dockerhub...'
docker push redbeandock/stowdo-backend:"${STOWDO_VERSION}"
echop 'Done'