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

### 📂 Структура проекта
- `core/` — настройки проекта Django.
- `notes/` — логика API (Models, ViewSets, Serializers).
- `static/` — фронтенд (HTML/JS).
- `setup.sh` — скрипт автоматизации развертывания.
- `requirements.txt` — список зависимостей.

```
