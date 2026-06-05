FROM python:3.13-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# App user
RUN useradd --system --create-home --shell /bin/bash travelpro

WORKDIR /app

# Python deps
COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir -r requirements/production.txt

# Node deps + build CSS
COPY package*.json ./
RUN npm ci --silent
COPY static/css/src/ static/css/src/
RUN npm run css:build

# App code
COPY --chown=travelpro:travelpro . .

# Create log/run dirs
RUN mkdir -p /var/log/travelpro /run/travelpro \
    && chown travelpro:travelpro /var/log/travelpro /run/travelpro

USER travelpro

ENV DJANGO_SETTINGS_MODULE=config.settings.production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "config.wsgi:application"]
