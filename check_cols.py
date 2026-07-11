import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.db import connection
cursor = connection.cursor()

# Get all tables
tables = connection.introspection.table_names()
print("ALL TABLES:", [t for t in tables if t.startswith("core") or t.startswith("faq") or t.startswith("hotels")])

