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

# 2. Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создаем виртуальное окружение venv..."
    python3 -m venv venv
else
    echo "ℹ️ Виртуальное окружение уже существует."
fi

# 3. Активация venv и установка зависимостей
echo "📥 Обновление pip и установка зависимостей из requirements.txt..."
source venv/bin/activate
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ Файл requirements.txt не найден! Устанавливаю базу вручную..."
    pip install django djangorestframework django-cors-headers
fi

# 4. Работа с БД
echo "🗄 Подготовка базы данных..."
python manage.py makemigrations notes
python manage.py migrate

# 5. Итог
echo ""
echo "✅ Проект успешно настроен!"
echo "------------------------------------------------"
echo "Для запуска выполните:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo "------------------------------------------------"