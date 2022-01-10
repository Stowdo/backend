#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

set -a
. .env
set +a

export STOWDO_DB_HOST='localhost'

python3 stowdo/manage.py makemigrations