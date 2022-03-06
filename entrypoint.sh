#!/bin/sh

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:3000 eventmanager.wsgi -w 3 --timeout 240  --worker-connections=100
