# Security Best Practices

## Шифрование

### AES-256
```python
from app.utils.encryption import DataEncryption

# Encrypt sensitive data
enc = DataEncryption()
encrypted_email = enc.encrypt("user@example.com")

# Decrypt
decrypted_email = enc.decrypt(encrypted_email)
```

### HTTPS/TLS
- Все соединения должны быть зашифрованы
- Использовать TLS 1.2 или выше
- Валидные сертификаты

## Аутентификация

### JWT токены
```python
from app.utils.security import create_access_token, verify_token

# Create token
token = create_access_token(
    data={"sub": "username", "id": 1, "role": "admin"}
)

# Verify token
payload = verify_token(token)
```

### Требования к паролям
- Минимум 12 символов
- Должен содержать: буквы, цифры, спецсимволы
- Использовать bcrypt для хэширования

## Управление доступом (RBAC)

```python
from app.utils.rbac import PermissionChecker, UserRole

# Check permission
can_create = PermissionChecker.can_create_pass(UserRole.ADMIN)

if not can_create:
    raise HTTPException(status_code=403, detail="Access denied")
```

## Логирование и аудит

```python
from app.utils.audit import AuditLogger

# Log action
await AuditLogger.log_action(
    db, 
    user_id=1,
    action="CREATE",
    entity_type="Pass",
    entity_id="pass_uuid",
    changes={"created": {"name": "John Doe"}}
)
```

## Валидация входных данных

- Всегда валидировать входные данные
- Использовать Pydantic schemas
- Проверять типы и размеры
- Санитизировать строки

## Защита от атак

### CSRF
- Использовать CSRF токены для изменений
- Проверять Referer и Origin headers

### XSS
- Экранировать HTML-содержимое
- Использовать Content Security Policy (CSP)
- Валидировать и санитизировать входные данные

### SQL Injection
- Использовать параметризованные запросы (SQLAlchemy ORM)
- Никогда не конкатенировать строки в SQL

### Rate Limiting
```python
# Middleware в main.py
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
```

## Резервное копирование

- Ежедневное резервное копирование
- Тестирование восстановления
- Шифрование резервных копий
- Хранение в защищённом месте

## Мониторинг и оповещение

- Мониторить логи на аномалии
- Оповещение о критических ошибках
- Отслеживание попыток несанкционированного доступа
- Метрики производительности

## Обновления безопасности

- Регулярно обновлять зависимости
- Мониторить CVE
- Применять патчи оперативно

## Переменные окружения

```bash
# Использовать .env для секретов
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_32_char_encryption_key
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## TLS Certificate

В production:
```bash
# Использовать Let's Encrypt
certbot certonly --standalone -d yourdomain.com

# Обновлять сертификат автоматически
0 0 1 * * certbot renew --quiet
```
