#!/bin/sh

#Set Environment
export DJANGO_SETTINGS_MODULE=gladminds.dev_settings

#bin/django collectstatic
# Pull latest code changes from Github
#git pull origin master

# Run buildout
bin/buildout

# Synchromize database
bin/django syncdb

# Run collectstatic
echo  yes |bin/django collectstatic

# Load the SMS Template
bin/django loaddata etc/data/template.json

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
nohup bin/fab runserver &
sleep 5
output=`ps aux | grep "bin/django r[u]nserver 0.0.0.0:8000"`
set -- $output
pid=$2
echo "Started gladminds (PID $pid)"
