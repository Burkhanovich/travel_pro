import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.db import connection
cursor = connection.cursor()
try:
    desc = connection.introspection.get_table_description(cursor, 'core_contactsettings')
    print("COLS:", [col.name for col in desc])
except Exception as e:
    print("ERROR:", e)
