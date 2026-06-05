# Travel Pro – Multi-Language Tour Agency Website

A production-ready Django 5 travel agency platform with multilingual support (EN, UZ, RU, IT, ES, JA), tour/hotel/MICE booking, Celery async tasks, Cloudinary media, and Tailwind CSS frontend.

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Node.js 18+ (for Tailwind CSS compilation)

### 2. Clone & create virtual environment

```bash
git clone <repo-url> travel_pro
cd travel_pro
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your DATABASE_URL, REDIS_URL, Cloudinary credentials, etc.
```

### 4. Database setup

```bash
# Create PostgreSQL database
createdb travel_pro

# Run migrations
python manage.py migrate --settings=config.settings.development

# Create translation fields (modeltranslation)
python manage.py sync_translation_fields
python manage.py update_translation_fields
```

### 5. Seed sample data

```bash
python manage.py seed_data
# Creates: admin/admin123, 30 tours, 10 countries, 15 hotels, 5 articles, 20 reviews
```

### 6. Compile static files & Tailwind

```bash
# Install Tailwind (one-time)
npm install -D tailwindcss @tailwindcss/typography @tailwindcss/forms

# Watch mode (development)
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

# Or collect static
python manage.py collectstatic --noinput
```

### 7. Start development server

```bash
python manage.py runserver
```

Open: http://localhost:8000  
Admin: http://localhost:8000/admin/ (admin / admin123)

---

## Celery Workers

```bash
# Start Celery worker (async emails)
celery -A config worker -l info

# Start Celery Beat (scheduled tasks)
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## Project Structure

```
travel_pro/
├── config/
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── development.py   # Debug tools, console email
│   │   └── production.py    # Security hardening, Sentry
│   ├── urls.py              # Root URL config
│   └── celery.py            # Celery app
├── apps/
│   ├── core/                # Base models, context processors, sitemaps
│   ├── tours/               # Tour packages, itineraries, departures
│   ├── destinations/        # Continents, countries, cities, attractions
│   ├── hotels/              # Hotels, rooms, amenities
│   ├── bookings/            # Inquiries, booking forms, async emails
│   ├── mice/                # Corporate / MICE packages
│   ├── guides/              # Travel articles with CKEditor
│   ├── reviews/             # Moderated reviews & ratings
│   └── accounts/            # User profiles
├── templates/               # All HTML templates
├── static/                  # CSS / JS assets
└── media/                   # User-uploaded files (dev only)
```

---

## Key Features

| Feature | Implementation |
|---------|---------------|
| **6 Languages** | django-modeltranslation + django-rosetta |
| **Booking System** | Multi-step form, Celery email tasks |
| **Filterable Tours** | django-filter with URL-persistent GET params |
| **Map View** | Leaflet.js with OpenStreetMap |
| **Rich Content** | CKEditor for articles/guides |
| **SEO** | Schema.org JSON-LD, sitemaps, OG tags |
| **Admin** | django-import-export, inline editing, bulk actions |
| **Media** | Cloudinary storage with Pillow processing |
| **Rate Limiting** | django-ratelimit (5/h on booking forms) |
| **Error Tracking** | Sentry integration |
| **Caching** | Redis: 5min tours list, 10min home page |
| **CSP** | django-csp security headers |

---

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` (dev) / `False` (prod) |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `CLOUDINARY_URL` | Cloudinary connection string |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `SENTRY_DSN` | Sentry project DSN |
| `ADMIN_URL` | Custom admin path (production) |

---

## Running Tests

```bash
pytest
# or
python manage.py test
```

---

## Deployment

1. Set `DEBUG=False` and configure `ALLOWED_HOSTS`
2. Set `DJANGO_SETTINGS_MODULE=config.settings.production`
3. Run `python manage.py collectstatic`
4. Use gunicorn: `gunicorn config.wsgi:application --bind 0:8000`
5. Set up Nginx as reverse proxy
6. Configure SSL certificate (Let's Encrypt)

---

## Languages

Access any page with language prefix:  
`/en/tours/`, `/uz/tours/`, `/ru/tours/`, `/it/tours/`, `/es/tours/`, `/ja/tours/`

Manage translations: http://localhost:8000/rosetta/
