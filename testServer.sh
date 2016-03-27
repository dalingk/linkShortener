#!/bin/sh
touch /tmp/app
uwsgi --http :8080 -H /var/www/bottle/.env --touch-reload /tmp/app --wsgi-file app.py
