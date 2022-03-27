#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

echop 'Welcome to Stowdo setup.'
echop 'This script will let you define variables for your local environment.'
echop 'The proposals in brackets are the default values. Leave blank to use them.'

echo
read -p 'Environment (DEVELOPMENT): ' environment
read -p 'Database name (stowdo): ' db_name
read -p 'Database host (localhost): ' db_host
read -p 'Database port (5432): ' db_port
read -p 'Database user (stowdo_api): ' db_user
read -sp 'Database password (auto generated): ' db_password && echo
read -sp 'Django secret key (auto generated):' secret_key && echo
read -p 'Minio host (localhost:9000): ' minio_host
read -p 'Minio access key (auto generated): ' minio_access_key
read -sp 'Minio secret key (auto generated):' minio_secret_key && echo
echo

if [ -z "$environment" ]
then
    environment=DEVELOPMENT
fi

if [ -z "$db_name" ]
then
    db_name=stowdo_api
fi

if [ -z "$db_host" ]
then
    db_host=localhost
fi

if [ -z "$db_port" ]
then
    db_port=5432
fi

if [ -z "$db_user" ]
then
    db_user=stowdo_api
fi

if [ -z "$db_password" ]
then
    db_password=$(openssl rand -base64 48)
fi

if [ -z "$secret_key" ]
then
    secret_key=$(openssl rand -base64 48)
fi

if [ -z "$minio_host" ]
then
    minio_host='localhost:9000'
fi

if [ -z "$minio_api_key" ]
then
    minio_access_key=$(openssl rand -base64 48)
fi

if [ -z "$minio_secret_key" ]
then
    minio_secret_key=$(openssl rand -base64 48)
fi

version=$(cat VERSION)

echo "STOWDO_VERSION=$version" > .env
echo "STOWDO_SECRET_KEY=$secret_key" >> .env
echo "STOWDO_ENVIRONMENT=$environment" >> .env
echo "STOWDO_DB_NAME=$db_name" >> .env
echo "STOWDO_DB_HOST=$db_host" >> .env
echo "STOWDO_DB_PORT=$db_port" >> .env
echo "STOWDO_DB_USER=$db_user" >> .env
echo "STOWDO_DB_PASSWORD=$db_password" >> .env
echo "MINIO_HOST=$minio_host" >> .env
echo "MINIO_ACCESS_KEY=$minio_access_key" >> .env
echo "MINIO_SECRET_KEY=$minio_secret_key" >> .env

echop 'Environment variables have been defined!'