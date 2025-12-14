# Pass System - Архитектура

## Обзор

Проект использует классическую трехслойную архитектуру:

```
┌─────────────────────────────────────────┐
│  Frontend (Vue 3, Mobile, PWA)          │
├─────────────────────────────────────────┤
│  API Gateway (REST/GraphQL)             │
├─────────────────────────────────────────┤
│  Backend Services (FastAPI)             │
├─────────────────────────────────────────┤
│  Database (PostgreSQL) + Cache (Redis)  │
└─────────────────────────────────────────┘
```

## Компоненты

### 1. Backend (FastAPI)
- REST API для всех операций
- GraphQL для сложных запросов
- Асинхронная обработка с Celery
- WebSocket для real-time уведомлений

### 2. Database (PostgreSQL)
- Реляционная модель данных
- Поддержка JSON для гибкости
- Индексы для оптимизации
- Логирование всех изменений

### 3. Cache (Redis)
- Кеширование часто запрашиваемых данных
- Сессии пользователей
- Очереди для async задач

### 4. Frontend
- Admin Dashboard (Vue 3 + Vite)
- Guard Scanner (Vue 3 + PWA)
- Guest Portal (Vue 3 + Vite)

## Безопасность

- JWT для аутентификации
- AES-256 для шифрования ПДн
- RBAC для управления доступом
- Логирование аудита
- CORS и CSRF защита
- Rate limiting

## Масштабируемость

- Horizontal scaling с Kubernetes
- Load balancing
- Database replication
- Cache invalidation
- Async task processing
