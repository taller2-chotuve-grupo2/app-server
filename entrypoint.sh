#!/bin/sh

# echo "Waiting for postgres..."

# while ! nc -z db 5432; do
#   sleep 0.1
# done

# echo "PostgreSQL started"

# python app.py
# flask run
gunicorn -b 0.0.0.0 run:app 