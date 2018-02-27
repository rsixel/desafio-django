#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

export BROKER_URL=amqp://admin:mypass@rabbit//

cd home_site
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m myuser -c "celery worker -A home_site -l info"