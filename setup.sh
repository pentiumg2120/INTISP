#!/bin/bash

# Скрипт автоматической настройки Secret Notes

# Останавливать выполнение при любой ошибке
set -e

echo "🚀 Начинаем настройку проекта..."

# 1. Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Ошибка: Python3 не установлен."
    exit 1
fi

# 2. Проверка Docker (для PostgreSQL)
if ! command -v docker &> /dev/null; then
    echo "❌ Ошибка: Docker не установлен. Установите Docker для запуска PostgreSQL."
    exit 1
fi

# 3. Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создаем виртуальное окружение venv..."
    python3 -m venv venv
else
    echo "ℹ️ Виртуальное окружение уже существует."
fi

# 4. Активация venv и установка зависимостей
echo "📥 Обновление pip и установка зависимостей из requirements.txt..."
source venv/bin/activate
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ Файл requirements.txt не найден! Устанавливаю базу вручную..."
    pip install django djangorestframework django-cors-headers
fi

# 5. Создание .env из примера, если его нет
if [ ! -f ".env" ]; then
    echo "📝 Копирую .env.example в .env..."
    cp .env.example .env
fi

# 6. Запуск PostgreSQL в Docker
echo "🐘 Запуск PostgreSQL в Docker..."
docker compose up -d db

# 7. Ожидание готовности БД
echo "⏳ Ожидание готовности PostgreSQL..."
until docker compose exec -T db pg_isready -U postgres > /dev/null 2>&1; do
    sleep 1
done
echo "✅ PostgreSQL готов."

# 8. Миграции
echo "🗄 Применение миграций..."
python manage.py makemigrations notes
python manage.py migrate

# 9. Итог
echo ""
echo "✅ Проект успешно настроен!"
echo "------------------------------------------------"
echo "Для запуска выполните:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo "------------------------------------------------"