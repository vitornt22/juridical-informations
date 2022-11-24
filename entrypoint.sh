#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

source /webapps/.venv/bin/activate
python3 manage.py makemigrations
blabla
python3 manage.py migrate

exec "$@"
