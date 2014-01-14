#!/bin/sh

#Set Environment
export DJANGO_SETTINGS_MODULE=gladminds.prod_settings

#bin/django collectstatic
# Pull latest code changes from Github
#git pull origin master

# Bootstrap setup
python bootstrap.py

# Run buildout
bin/buildout -o

# Synchromize database
#bin/fab syncdb

# Run collectstatic
#bin/fab collectstatic

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

# Run server
echo "Starting gladminds ..."
nohup bin/fab runserver &
sleep 5
output=`ps aux | grep "bin/django r[u]nserver 0.0.0.0:8000"`
set -- $output
pid=$2
echo "Started gladminds (PID $pid)"
