# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Устанавливаем переменные окружения для Flask
ENV FLASK_APP=todoapp
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=production

# Открываем порт 5000
EXPOSE 5000

# Команда запуска:
# 1. Обновляем базу данных через миграции
# 2. Запускаем сервер
CMD flask db upgrade && flask run
