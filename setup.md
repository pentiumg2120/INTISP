### 🚀 Быстрый старт

Если вы используете Linux/macOS, просто запустите скрипт настройки:

```bash
chmod +x setup.sh
./setup.sh

```

Затем запустите сервер:

```bash
source venv/bin/activate
python manage.py runserver

```

Проект будет доступен по адресу: `http://127.0.0.1:8000/`

---

### 📡 API Endpoints

| Метод | Путь | Описание |
| :--- | :--- | :--- |
| `POST` | `/api/notes/` | Создать заметку (принимает `content`, `max_views`, `password`) |
| `GET` | `/api/notes/{id}/` | Получить заметку (опционально: `?password=...`) |

---

### 🐘 База данных

Проект использует PostgreSQL 16 в Docker-контейнере. Конфигурация подключения — через переменную `DATABASE_URL` в `.env` (копируется из `.env.example` при первом запуске `setup.sh`).

Управление контейнером вручную:

```bash
docker compose up -d db       # Запустить PostgreSQL
docker compose down           # Остановить и удалить контейнер
docker compose down -v        # Удалить контейнер и том с данными
```

---

### 📂 Структура проекта
- `core/` — настройки проекта Django.
- `notes/` — логика API (Models, ViewSets, Serializers).
- `static/` — фронтенд (HTML/JS).
- `docker-compose.yml` — контейнер PostgreSQL.
- `.env.example` — пример переменных окружения.
- `setup.sh` — скрипт автоматизации развертывания.
- `requirements.txt` — список зависимостей.

```
