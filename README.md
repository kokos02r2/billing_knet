# Billing KNet

## Описание проекта

Billing KNet – это система управления биллингом, разработанная на Django. Она предоставляет API и веб-интерфейс для управления тарифами, расчетами и платежами пользователей.

### Основные функции:

- Управление пользователями и их тарифами
- Автоматический расчет и перерасчет стоимости услуг
- Генерация счетов и уведомлений
- Интеграция с платежными системами
- API для взаимодействия с внешними сервисами

## Установка и настройка

### Требования

- Python 3.9+
- PostgreSQL
- Poetry (для управления зависимостями)

### Установка

1. Клонируйте репозиторий:

   ```bash
   git clone <репозиторий>
   cd billing_knet-main
   ```

2. Установите зависимости с помощью Poetry:

   ```bash
   poetry install
   ```

3. Настройте переменные окружения (можно использовать `.env` файл):

   ```
   DATABASE_URL=postgres://user:password@localhost:5432/billing_db
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

4. Примените миграции базы данных:

   ```bash
   poetry run python billing/manage.py migrate
   ```

5. Создайте суперпользователя:

   ```bash
   poetry run python billing/manage.py createsuperuser
   ```

6. Заполните базу тестовыми данными (если требуется):
   ```bash
   poetry run python billing/manage.py loaddata initial_data.json
   ```

## Запуск проекта

1. Запустите сервер разработки:

   ```bash
   poetry run python billing/manage.py runserver
   ```

2. Открывайте приложение по адресу `http://127.0.0.1:8000/`.

## API

### Основные эндпоинты:

- **Аутентификация:** `/api/auth/login/`, `/api/auth/logout/`
- **Пользователи:** `/api/users/` – управление пользователями
- **Тарифы:** `/api/tariffs/` – управление тарифами
- **Счета:** `/api/bills/` – информация о платежах и счетах

API поддерживает аутентификацию через JWT-токены. Для получения токена выполните:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -d '{"username": "admin", "password": "admin"}' -H "Content-Type: application/json"
```

## Использование

- Админ-панель: `http://127.0.0.1:8000/admin/`
- API-документация: `http://127.0.0.1:8000/api/docs/` (если включен Swagger)

## Структура проекта

```
billing_knet-main/
│── billing/
│   ├── manage.py        # Точка входа Django
│   ├── core/            # Основной модуль
│   │   ├── settings.py  # Настройки Django
│   │   ├── urls.py      # Маршруты
│   │   ├── views.py     # Представления
│   │   ├── helpers/     # Вспомогательные модули
│   │   ├── tests/       # Тесты
│── poetry.lock          # Зависимости проекта
│── pyproject.toml       # Конфигурация Poetry
│── setup.cfg            # Конфигурация пакета
│── .gitignore           # Игнорируемые файлы
```

## Тестирование

Для запуска тестов выполните:

```bash
poetry run python billing/manage.py test
```

## Развертывание

### Запуск через Gunicorn и Nginx

1. Установите Gunicorn:
   ```bash
   poetry add gunicorn
   ```
2. Запустите сервер Gunicorn:
   ```bash
   poetry run gunicorn billing.core.wsgi:application --bind 0.0.0.0:8000
   ```
3. Настройте Nginx для проксирования запросов к Gunicorn.

### Использование Docker

1. Соберите Docker-образ:
   ```bash
   docker build -t billing_knet .
   ```
2. Запустите контейнер:
   ```bash
   docker run -p 8000:8000 --env-file .env billing_knet
   ```

## Поддержка и развитие

Если у вас есть вопросы или предложения, создайте issue в репозитории или свяжитесь с разработчиком.

## Лицензия

Этот проект распространяется под лицензией MIT.
