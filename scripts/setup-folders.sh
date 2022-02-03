#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

echop 'Creating needed folders...'
mkdir db-data
mkdir minio-data
mkdir proxy-data
mkdir letsencrypt
echop 'Done'