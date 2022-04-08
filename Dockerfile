FROM python:3.8-alpine3.15

WORKDIR /app

COPY Pipfile /app
COPY Pipfile.lock /app
COPY stowdo /app

RUN \
    apk add --no-cache bash postgresql-libs jpeg-dev && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev zlib-dev g++ libffi-dev && \
    pip install pipenv && \
    pipenv install --deploy --system && \
    pip uninstall pipenv -y && \
    apk --purge del .build-deps

EXPOSE 8000