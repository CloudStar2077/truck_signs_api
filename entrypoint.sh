#!/usr/bin/env bash
set -e

# Exit immediately if a command exits with a non-zero status

echo "==> Waiting for PostgreSQL to be ready..."

# Loop until a successful connection to PostgreSQL can be established
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        dbname=os.environ['DOCKER_DB_NAME'],
        user=os.environ['DOCKER_DB_USER'],
        password=os.environ['DOCKER_DB_PASSWORD'],
        host=os.environ['DOCKER_DB_HOST'],
        port=os.environ['DOCKER_DB_PORT'],
    )
except psycopg2.OperationalError:
    sys.exit(1)
"; do
  echo "   PostgreSQL not ready – retrying in 2 s..."
  sleep 2
done

echo "   PostgreSQL is ready."

echo "==> Running migrations..."

# Apply Django database migrations
python manage.py migrate --noinput

echo "==> Collecting static files..."

# Collect static files into STATIC_ROOT
python manage.py collectstatic --noinput

echo "==> Creating superuser (skipped if already exists)..."

# Create a Django superuser if it does not already exist
python manage.py shell << 'PYEOF'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]
email    = os.environ["DJANGO_SUPERUSER_EMAIL"]
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

# Check if the user already exists before creating it
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists – skipping.")
PYEOF

echo "==> Starting Gunicorn on port 8020..."

# Start Gunicorn application server
exec gunicorn truck_signs_designs.wsgi:application \
    --bind 0.0.0.0:8020 \
    --workers 3 \
    --timeout 120