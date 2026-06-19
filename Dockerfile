# syntax=docker/dockerfile:1

FROM python:3.12-slim

# ── Системные зависимости ──────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ── Пользователь без рута ──────────────────────────────────────
RUN groupadd -r app && useradd -r -g app -d /app app

WORKDIR /app

# ── Зависимости Python (кэшируются при пересборке) ─────────────
COPY requirements.txt .
RUN pip config --user set global.index-url https://pypi-mirror.gitverse.ru/simple/ \
    && pip config --user set global.trusted-host pypi-mirror.gitverse.ru \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn==23.0.0

# ── Код приложения ─────────────────────────────────────────────
COPY . .

# ── Права ──────────────────────────────────────────────────────
RUN chown -R app:app /app
USER app

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "172.0.0.1:8000"]
