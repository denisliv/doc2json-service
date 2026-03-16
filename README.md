# Doc2JSON Service

Самостоятельный сервис для обработки PDF-документов: OCR, маршрутизация, извлечение структурированных данных в JSON.

## Быстрый старт

```bash
docker compose up --build
```

Создание администратора (выполняется один раз после первого запуска):

```bash
docker compose exec backend python create_admin.py admin changeme "Administrator"
```

Сервис будет доступен:
- **UI**: http://localhost
- **API**: http://localhost:8000/api/v1
- **Swagger**: http://localhost:8000/docs

## Архитектура

| Компонент | Технология | Порт |
|-----------|-----------|------|
| Frontend | Nginx + HTML/CSS/JS | 80 |
| Backend | FastAPI | 8000 |
| Worker | Celery | — |
| Database | PostgreSQL 17 | 5432 |
| Broker | Redis 7 | 6379 |

Внешние сервисы (не в Docker Compose):
- **vLLM PaddleOCR-VL** — OCR (порт 8118)
- **vLLM LLM** — маршрутизация и извлечение (порт 11434)

## API

### Документы
- `POST /api/v1/documents/process` — загрузить PDF, запустить обработку
- `GET /api/v1/documents/jobs/{id}` — статус и результат задания

### OCR (без аутентификации)
- `POST /api/v1/ocr/extract-text` — PDF → Markdown
- `POST /api/v1/ocr/extract-json` — PDF → JSON (полный pipeline)

### Валидация (без аутентификации)
- `POST /api/v1/validate` — валидация JSON по схеме типа документа

### Типы документов
- `GET /api/v1/document-types` — список типов
- `POST /api/v1/document-types` — создать новый тип (admin)

## Роли

| Роль | Возможности |
|------|------------|
| admin | Полный контроль, управление пользователями и типами |
| manager | Редактирование типов, просмотр всех заданий |
| operator | Загрузка документов, просмотр своих заданий |

## Миграции БД

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend alembic revision --autogenerate -m "description"
```
