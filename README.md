# Система записи к специалистам

Это приложение представляет собой систему записи к специалистам с веб-интерфейсом и Telegram ботом.

## Функциональность

- Запись к специалистам через веб-интерфейс
- Интеграция с Telegram ботом
- Управление расписанием специалистов
- Профиль пользователя
- Выбор услуг
- Выбор времени записи

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.venv\Scripts\activate  # для Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

1. Запустите веб-приложение:
```bash
python start_webapp.py
```

2. Запустите Telegram бота:
```bash
python bot/main_b.py
```

## Структура проекта

- `webapp/` - веб-приложение на Flet
- `bot/` - Telegram бот
- `database/` - файлы базы данных
- `storage/` - хранилище данных
- `requirements.txt` - зависимости проекта

## Технологии

- Python
- Flet (веб-интерфейс)
- aiogram (Telegram бот)
- SQLite (база данных)
