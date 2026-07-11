import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.db import connection
cursor = connection.cursor()

tables_to_drop = [
    'core_heroslide',
    'hotels_hotel_amenities',
    'hotels_hotelimage',
    'hotels_hotelroom',
    'hotels_hotel',
    'hotels_hotelamenity'
]

for table in tables_to_drop:
    print(f"Dropping table {table}...")
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
    except Exception as e:
        print(f"Error dropping {table}: {e}")

connection.commit()

# Get all tables
tables = connection.introspection.table_names()
print("AFTER DROP - ALL TABLES:", [t for t in tables if t.startswith("core") or t.startswith("faq") or t.startswith("hotels")])


