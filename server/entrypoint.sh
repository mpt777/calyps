#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py makemigrations --merge --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py initadmin
python manage.py initialize_data

exec "$@"
