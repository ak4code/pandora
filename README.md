# Pandora

Django-конфигурационный сервис. Каркас проекта: настройки, URL-конфиг, WSGI/ASGI-входы,
инфраструктура uv + ruff + ty + pre-commit + pytest и CI.

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Переменные окружения

| Название        | По умолчанию | Назначение                                              |
|-----------------|--------------|---------------------------------------------------------|
| `DEBUG`         | `true`       | Режим отладки Django                                    |
| `SECRET_KEY`    | dev-ключ     | Секретный ключ; в продакшене обязателен собственный ключ |
| `ALLOWED_HOSTS` | пусто        | Числовой список хостов через запятую                    |
| `DATABASE_PATH` | `db.sqlite3` | Путь к файлу SQLite относительно корня проекта          |

`SettingsError` поднимается при запуске, если `DEBUG=0` без собственного `SECRET_KEY`
(dev-fallback), или если `DEBUG=0` и `ALLOWED_HOSTS` пуст.

## Быстрый старт

```bash
uv sync
uv run python manage.py check
uv run python manage.py migrate
uv run python manage.py runserver
```

## Тесты и качество

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run ty check .
uv run pre-commit run --all-files
```

## Структура

- `config/` — корневой пакет проекта: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
- `tests/` — pytest-тесты (smoke-тест `manage.py check`)
- `.github/workflows/ci.yml` — CI: pre-commit, ruff, ty, `manage.py check`, pytest

## Планы

- REST-фронтенд DRF (селекторы/сервисы по архитектуре Services & Selectors)
- PostgreSQL вместо SQLite через `DATABASE_URL`
- Celery-квора для асинхронных задач
