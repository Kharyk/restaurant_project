FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt python-decouple

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "--log-level=info", "restaurant.wsgi:application"]