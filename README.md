
# Stowdo

Django-based website to host files online.

## Requirements

This project requires at least [Python 3.8](https://www.python.org/downloads/) to run.

But if you intend to use the provided scripts (recommended) you also need [Pipenv](https://pypi.org/project/pipenv/) and [Docker](https://www.docker.com/get-started/).

For Debian users, you can run the following command to install Pipenv and Python 3.8:

```bash
$ apt install python3.8 pipenv docker-ce
```

> For older Debian versions or Ubuntu based distributions, `docker-ce` exists under the name `docker.io` or `docker`.

## Installation

> Scripts found in `scripts` folder are made to work on GNU/Linux distributions. **They may not work on other operating systems**.

First clone this repo:

```bash
$ git clone git@github.com:Stowdo/backend.git
$ cd backend
```

Setup environment variables:

```bash
$ ./scripts/setup-env.sh
```

Finally setup a virtual environment with its dependencies:

```bash
$ ./scripts/setup-deps.sh
```

## Run Locally

First navigate to the project root directory:

```bash
$ cd path/to/stowdo/backend
```

Then start Stowdo:

```bash
$ ./scripts/run-dev.sh
```

Stowdo API is now locally accessible at `http://localhost:8000/`.

## Clean

To clean docker containers and images created by the project:

```bash
$ ./scripts/clean-docker.sh
```

## Tech Stack

**API:** Python 3, Django, Django-rest-framework

**Databases:** Minio, Postgresql

**Deploy:** Docker

## Environment Variables

Local environment variables are stored in `.env` file.

**`STOWDO_VERSION`**

The current version of Stowdo.

**`STOWDO_SECRET_KEY`**

A string used by Django to encode sensitive data. Default is auto-generated.

**`STOWDO_ENVIRONMENT`**

The current environment. Should be `DEVELOPMENT` or `PRODUCTION`. Default is `DEVELOPMENT`.

**`STOWDO_DB_NAME`**

The name of the database to store data. Default is `stowdo_api`.

**`STOWDO_DB_HOST`**

The hostname or address of the database to connect. Default is `localhost`.

**`STOWDO_DB_PORT`**

The port to use to connect to the database. Default is `5432`.

**`STOWDO_DB_USER`**

The user of the database. Default is `stowdo_api`.

**`STOWDO_DB_PASSWORD`**

The password used to authenticate to the database. Default is auto-generated.

**`MINIO_HOST`**

The hostname or address with the port of the Minio database. Default is `localhost:9000`.

**`MINIO_ACCESS_KEY`**

The public access key used to authenticate to the Minio database. Default is auto-generated.

**`MINIO_SECRET_KEY`**

The secret key used to secure the connection with the Minio database. Default is auto-generated.
