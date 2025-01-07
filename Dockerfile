FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Add Django debug mode
ENV DEBUG=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Split the commands and add error output redirection
RUN pwd
RUN ls -la
RUN python manage.py collectstatic --noinput --verbosity 2 2>&1 || (echo "Collectstatic failed with error: $?" && exit 1)

EXPOSE 8000
CMD ["gunicorn", "main:app", "--workers", "4", "--preload", "-b", '0.0.0.0:8000', "--log-level", "info"]