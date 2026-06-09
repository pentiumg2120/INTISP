### 🐳 Быстрый старт (Docker)

Весь проект запускается одной командой:

```bash
cp .env.example .env              # однократно
docker compose up --build
```

Проект будет доступен по адресу: `http://127.0.0.1:8000/`

---

### 🖥 Локальный запуск (без Docker)

Если вы используете Linux/macOS и предпочитаете запуск на хосте:

```bash
chmod +x setup.sh
./setup.sh

source venv/bin/activate
python manage.py runserver
```

---

### 📡 API Endpoints

| Метод | Путь | Описание |
| :--- | :--- | :--- |
| `POST` | `/api/notes/` | Создать заметку (принимает `content`, `max_views`, `password`) |
| `GET` | `/api/notes/{id}/` | Получить заметку (опционально: `?password=...`) |

---

### 🐘 База данных

Проект использует PostgreSQL 16 в Docker-контейнере. Конфигурация подключения — через переменную `DATABASE_URL` в `.env` (копируется из `.env.example`).

Управление контейнерами:

```bash
docker compose up --build        # Собрать и запустить всё
docker compose up -d db          # Только PostgreSQL
docker compose down              # Остановить контейнеры
docker compose down -v           # Удалить вместе с данными
```

---

### 📂 Структура проекта
- `core/` — настройки проекта Django.
- `notes/` — логика API (Models, ViewSets, Serializers).
- `static/` — фронтенд (HTML/JS).
- `Dockerfile` — сборка образа приложения.
- `entrypoint.sh` — скрипт входа (ожидание БД + миграции).
- `docker-compose.yml` — оркестрация веб-приложения и PostgreSQL.
- `.env.example` — пример переменных окружения.
- `.dockerignore` — исключения для Docker-контекста.
- `setup.sh` — скрипт локальной настройки.
- `requirements.txt` — список зависимостей.

```
