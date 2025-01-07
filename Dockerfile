FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN pwd && ls -la && \
    python manage.py collectstatic --noinput --verbosity 2

EXPOSE 8000
CMD ["gunicorn", "main:app", "--workers", "4", "--preload", "-b", '0.0.0.0:8000', "--log-level", "info"]