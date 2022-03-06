
# Stowdo

Django-based website to host files online.


## Installation

First clone this repo:

```bash
$ git clone git@github.com:RedbeanGit/stowdo.git
```

Setup environment variables:

```bash
$ ./scripts/setup-env.sh
```

#### Install to run with Docker compose

If you plan to run Stowdo inside a docker container then you just need to install [Docker compose](https://docs.docker.com/get-docker/).

#### Install to run with Python

You can also launch Stowo directly with your local Python interpreter.

First, install [Python 3.9](https://www.python.org/downloads/).

Navigate to the project root directory:

```bash
$ cd path/to/stowdo
```

Create and run a virtual environment (optional):

```bash
$ python3 -m venv env
$ . env/bin/activate
```

Setup Stowdo dependencies:

```bash
$ ./scripts/setup-deps.sh
```

#### Note for Windows users

Scripts call Python with the `python3` command. Unfortunately on Windows the correct command is simply `python`.

One way to solve this problem is to make a copy of `python.exe` named `python3.exe` in the same folder.

The default installation folder for Python 3.8 is `C:\Users\<youUsername>\AppData\Local\Programs\Python\Python39\`.

## Run Locally

First navigate to the project root directory:

```bash
$ cd path/to/stowdo
```

If you have installed a virtual environment, activate it:

```bash
$ . env/bin/activate
```

And start Stowdo:

```bash
$ ./scripts/run-dev.sh
```

## Clean

To clean docker containers and images created by the project:

```bash
$ ./scripts/clean-docker.sh
```

## Tech Stack

**API:** Python 3, Django, Django-rest-framework

**Databases:** Minio, Postgresql

## Environment Variables

Local environment variables are stored in `.env` file.

**`STOWDO_VERSION`**

The current version of Stowdo.

**`STOWDO_SECRET_KEY`**

A string used by Django to encode sensitive data. Default is auto-generated.

**`STOWDO_ENVIRONMENT`**

The current environment. Should be `DEVELOPMENT`, `STAGING` or `PRODUCTION`. Default is `DEVELOPMENT`.

**`STOWDO_DB_NAME`**

The name of the database to store data. Default is `stowdo`.

**`STOWDO_DB_HOST`**

The hostname or address of the database to connect. Default is `db`.

**`STOWDO_DB_PORT`**

The port to use to connect to the database. Default is `5432`.

**`STOWDO_DB_USER`**

The user of the database. Default is `postgres`.

**`STOWDO_DB_PASSWORD`**

The password used to authenticate to the database. Default is auto-generated.

**`MINIO_HOST`**

The hostname or address with the port of the Minio database. Default is `localhost:9000`.

**`MINIO_ACCESS_KEY`**

The public access key used to authenticate to the Minio database. Default is auto-generated.

**`MINIO_SECRET_KEY`**

The secret key used to secure the connection with the Minio database. Default is auto-generated.
