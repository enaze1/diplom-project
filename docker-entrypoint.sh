#!/bin/sh
set -eu

mkdir -p "$(dirname "${SQLITE_PATH:-/app/data/db.sqlite3}")"

python manage.py migrate --noinput
python manage.py seed_data
python manage.py collectstatic --noinput

exec gunicorn production_system.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}"
