#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

echop 'Setup temporary virtual environment with its dependencies...'
pipenv install

if [ $? -eq 0 ]
then
    echop 'Python packages have been installed!'
else
    errorp 'Unable to setup virtual environment. Do you have pipenv installed?'
fi

echo