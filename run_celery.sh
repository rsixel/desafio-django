#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

export BROKER_URL=amqp://admin:mypass@rabbit//

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m myuser -c "celery worker -A home_site -l info -Q default -n default@%h"