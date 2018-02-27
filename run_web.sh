#!/bin/sh

# wait for RabbitMQ to start
sleep 10


cd /app/home_site
pwd
ls
# prepare init migration
python3 manage.py makemigrations home_site
# migrate db, so we have the latest db schema
python3 manage.py migrate
# start development server on public ip interface, on port 8000
python3 manage.py runserver 0.0.0.0:8000