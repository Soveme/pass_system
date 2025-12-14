# Руководство по разработке

## Структура веток

Каждый пункт ТЗ развивается в отдельной ветке с минимум 2 коммитами:

1. `feature/project-setup` - Базовая структура
2. `feature/backend-api` - Backend API
3. `feature/database-schema` - Схема БД
4. `feature/qr-generation` - QR коды
5. `feature/admin-dashboard` - Админ-панель
6. `feature/guard-interface` - Интерфейс охраны
7. `feature/guest-interface` - Интерфейс гостей
8. `feature/security-encryption` - Безопасность
9. `feature/calendar-integration` - Календари
10. `feature/notifications` - Уведомления
11. `feature/testing-ci-cd` - Тестирование

## Правила разработки

- ✅ Никогда не коммитить напрямую в main
- ✅ Каждая ветка должна содержать не менее 2 коммитов
- ✅ Использовать Pull Requests для merge в main
- ✅ Прямые интеграции (email, SMS) реализовать как заглушки с выводом в консоль
- ✅ Каждый коммит должен содержать логичную часть работы

## Коммит сообщения

Формат: `[тип] описание`

Типы:
- `feat:` - новая функция
- `fix:` - исправление
- `refactor:` - рефакторинг
- `docs:` - документация
- `test:` - тесты
- `chore:` - конфигурация

Примеры:
- `feat: Add guest pass generation API`
- `feat: Implement QR code scanner for guards`
- `refactor: Move encryption logic to utils`

## Локальная разработка

```bash
# Клонирование
git clone https://github.com/Soveme/pass_system.git
cd pass_system

# Создание ветки
git checkout -b feature/your-feature

# Разработка...

# Коммиты
git add .
git commit -m "feat: your feature description"

# Push и создание PR
git push origin feature/your-feature
```
