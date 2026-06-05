web: gunicorn --config gunicorn.conf.py config.wsgi:application
worker: celery -A config.celery worker --loglevel=warning --concurrency=2
beat: celery -A config.celery beat --loglevel=warning --scheduler django_celery_beat.schedulers:DatabaseScheduler
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
