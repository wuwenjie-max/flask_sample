#!/bin/sh

echo "start flask server"
gunicorn -c config/gun.conf server:app

# 选择是否开启celery
#echo "start celery job"
#celery -A celery_server worker -l INFO -c 4 -D -f ./log/celery.log --pidfile celery.pid