#!/bin/bash
set -e

# Ждём PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
until pg_isready -h db -U postgres -d intisp -q 2>/dev/null; do
    sleep 1
done
echo "✅ PostgreSQL is ready"

# Миграции
echo "🗄 Running migrations..."
python manage.py migrate --noinput

# Запуск переданной команды
exec "$@"
