#!/bin/sh

export DJANGO_SETTINGS_MODULE=gladminds.dev_settings
bin/buildout
echo  yes |bin/django collectstatic --settings=$DJANGO_SETTINGS_MODULE

bin/django setup --settings=$DJANGO_SETTINGS_MODULE
bin/django gm_migrate --settings=$DJANGO_SETTINGS_MODULE
bin/django load_gm_migration_data --settings=$DJANGO_SETTINGS_MODULE
# Load the SMS Template
#bin/django loaddata etc/data/template.json --settings=$DJANGO_SETTINGS_MODULE

#load services
bin/django service_setup

# TODO: Stop already running server
output=`ps aux | grep "bin/django r[u]nserver 0.0.0.0:8000"`
set -- $output
pid=$2
echo "Stopping gladminds (PID $pid) ..."
kill $pid
sleep 2
kill -9 $pid >/dev/null 2>&1
sleep 5
echo "Stopped gladminds"

#Stopped Celery
echo Stopping celery and celery beat ..
ps -ef | grep celery | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
sleep 3

#Starting Celery and Celery beat ...
echo Starting Celery and Celery beat ...
nohup bin/django celery -A gladminds worker --loglevel info -f tasks.out --settings=$DJANGO_SETTINGS_MODULE & > /dev/null 2>&1
nohup bin/django celery -A gladminds beat -S djcelery.schedulers.DatabaseScheduler --loglevel info -f beat.out --settings=$DJANGO_SETTINGS_MODULE & > /dev/null 2>&1
sleep 5

# Run server
echo "Starting gladminds ..."
nohup bin/django runserver --settings=$DJANGO_SETTINGS_MODULE &
sleep 5
output=`ps aux | grep "bin/django r[u]nserver 0.0.0.0:8000"`
set -- $output
pid=$2
echo "Started gladminds (PID $pid)"
