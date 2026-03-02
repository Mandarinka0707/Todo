# Todo List API (Python, FastAPI)

Простое API на **Python + FastAPI** для управления задачами (Todo list) с возможностью:

- **добавления задач**
- **редактирования задач**
- **удаления задач**
- **установки приоритета** (1 – высокий, 2 – средний, 3 – низкий)
- **установки срока выполнения (дедлайна)**

База данных: **PostgreSQL**, ORM: **SQLAlchemy**, контейнеризация: **Docker + docker-compose**.

## Запуск через Docker

1. Установите Docker и Docker Compose.
2. В корне проекта (`c:\Users\Katana\Desktop\Akutin\first`) выполните:

```bash
docker compose up --build
```

3. После старта контейнеров:
   - API будет доступно по адресу: `http://localhost:8000`
   - Документация Swagger: `http://localhost:8000/docs`

## Подключение к базе

По умолчанию используется строка подключения (через переменную окружения `DATABASE_URL` в `docker-compose.yml`):

```text
postgresql+psycopg2://warehouse:warehouse_password@db:5432/warehouse_db
```

Для локального запуска без Docker по умолчанию используется:

```text
postgresql+psycopg2://warehouse:warehouse_password@localhost:5432/warehouse_db
```

Вы можете заменить её через переменную окружения `DATABASE_URL`.

## Модель задачи (Todo)

Каждая задача содержит:

- `id` – идентификатор
- `title` – заголовок (обязательный)
- `description` – описание (опционально)
- `priority` – приоритет (1, 2 или 3; по умолчанию 3 – низкий)
- `due_date` – дедлайн (дата, опционально)
- `completed` – флаг выполнения (по умолчанию `false`)
- `created_at` – дата создания
- `updated_at` – дата последнего обновления

## API-эндпоинты Todo list

### GET

- **`/api/todos`** – получить список всех задач  
  Сортировка: сначала невыполненные, затем выполненные, внутри по приоритету (1 → 3) и по дедлайну.

- **`/api/todos/{id}`** – получить информацию о конкретной задаче

### POST

- **`/api/todos`** – создать новую задачу

Пример тела запроса:

```json
{
  "title": "Подготовить отчёт",
  "description": "Собрать данные по задачам",
  "priority": 1,
  "due_date": "2026-03-10"
}
```

### PUT

- **`/api/todos/{id}`** – обновить задачу (можно менять заголовок, описание, приоритет, срок и статус)

```json
{
  "title": "Подготовить итоговый отчёт",
  "description": "Обновлённое описание",
  "priority": 2,
  "due_date": "2026-03-12",
  "completed": true
}
```

### DELETE

- **`/api/todos/{id}`** – удалить задачу

### Health-check

- **`/health`** – простой эндпоинт проверки работоспособности сервиса

```json
{
  "status": "ok"
}
```

## Локальный запуск без Docker

1. Установите Python 3.12.
2. Создайте и активируйте виртуальное окружение (рекомендуется).
3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите PostgreSQL локально и создайте базу `warehouse_db` с пользователем `warehouse/warehouse_password` (или измените `DATABASE_URL` через переменную окружения).
5. Запустите приложение:

```bash
uvicorn app.main:app --reload
```

После этого API будет доступно на `http://localhost:8000`, а Swagger-документация – на `http://localhost:8000/docs`.

