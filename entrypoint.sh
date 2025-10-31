#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U $DB_USER; do
	sleep 1
done
echo "PostgreSQL is ready!"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Setting socket directory permissions..."
chmod 770 /run/sockets

echo "Starting Gunicorn..."
exec gunicorn --bind unix:/run/sockets/cooplink.sock \
	--workers 3 \
	--timeout 60 \
	--access-logfile - \
	--error-logfile - \
	core.wsgi:application
