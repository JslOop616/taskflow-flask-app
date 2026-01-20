# 📋 TaskFlow - Flask Task Management System

[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Live Demo](https://img.shields.io/badge/Demo-Live-green?logo=pythonanywhere&logoColor=white)](https://emikpro.pythonanywhere.com)
[![GitHub](https://img.shields.io/badge/Repository-GitHub-181717?logo=github&logoColor=white)](https://github.com/JslOop616/taskflow-flask-app)

Полнофункциональное веб-приложение для управления задачами с REST API, разработанное на Flask. Система включает аутентификацию пользователей, CRUD операции для задач, панель управления и полноценное REST API.

##  Основные возможности

###  Безопасность и аутентификация
- Регистрация и вход пользователей с валидацией данных
- Хеширование паролей с использованием Werkzeug
- Сессионная аутентификация через Flask-Login
- Защита маршрутов декоратором @login_required
<img width="1573" height="701" alt="image" src="https://github.com/user-attachments/assets/0cdc5fa8-61e1-404c-aded-c979d82f27ba" />

### 📝 Управление задачами
- Создание задач с заголовком, описанием и приоритетом
- Просмотр задач в удобной панели управления
- Редактирование статуса (выполнено/в процессе)
- Удаление задач с подтверждением
- Фильтрация задач по статусу и приоритету
<img width="1053" height="686" alt="image" src="https://github.com/user-attachments/assets/0b3bbaa6-7ebe-4428-ae45-92ba4184ba07" />

###  REST API
- Полный CRUD API для интеграции с другими системами
- JSON-формат всех ответов
- Аутентификация через сессии
- Документированные эндпоинты
<img width="1017" height="264" alt="image" src="https://github.com/user-attachments/assets/b6aaa857-9f76-4a85-8a03-8e1ecd08ae5e" />

###  Интерфейс пользователя
- Адаптивный дизайн на Bootstrap 5
- Мобильная версия для всех устройств
- Интуитивная навигация между разделами
- Визуальные индикаторы приоритета задач
<img width="1817" height="951" alt="image" src="https://github.com/user-attachments/assets/28841738-eabd-41e3-a9e2-8a2a133d6fd1" />

##  Технологический стек

### Backend
- Flask 3.1.2 - микрофреймворк для Python
- Flask-SQLAlchemy 3.0.5 - ORM для работы с базой данных
- Flask-Login 0.6.2 - управление аутентификацией пользователей
- Werkzeug 2.3.7 - утилиты для WSGI и безопасности
- SQLite - легковесная база данных (готова к миграции на PostgreSQL)

### Frontend
- HTML5 - семантическая разметка
- CSS3 с Bootstrap 5.1.3 - адаптивные стили
- JavaScript - динамическое поведение страниц
- Jinja2 - шаблонизатор Flask

### Инфраструктура
- PythonAnywhere - хостинг и деплоймент
- Git/GitHub - контроль версий
- Virtual Environment - изоляция зависимостей
- WSGI - интерфейс для развертывания
- 
##  Живая демонстрация

### Доступ к сайту
URL: [https://emikpro.pythonanywhere.com](https://emikpro.pythonanywhere.com)

### Тестовый аккаунт
Для быстрого ознакомления с функционалом используйте:
- Логин: test
- Пароль: test123

### Основные страницы
1. Главная (`/`) - информация о проекте
2. Регистрация (`/register`) - создание нового аккаунта
3. Вход (`/login`) - аутентификация пользователя
4. Панель управления (`/dashboard`) - управление задачами
5. API Health Check (`/api/health`) - проверка работы API

##  Документация API

### Базовый URL
### Эндпоинты

| Метод | Эндпоинт | Описание | Требуется аутентификация |
|-------|----------|----------|--------------------------|
| GET | /tasks | Получить все задачи пользователя | ✅ |
| GET | /tasks/<id> | Получить конкретную задачу | ✅ |
| POST | /tasks | Создать новую задачу | ✅ |
| PUT | /tasks/<id> | Обновить существующую задачу | ✅ |
| DELETE | /tasks/<id> | Удалить задачу | ✅ |
| GET | /health | Проверка работоспособности API | ❌ |
| GET | /user/info | Информация о текущем пользователе | ✅ |

