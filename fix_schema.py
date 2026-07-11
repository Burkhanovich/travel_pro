import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.db import connection
cursor = connection.cursor()

sqls = [
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels text DEFAULT '';",
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels_en text;",
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels_uz text;",
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels_ru text;",
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels_it text;",
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels_es text;",
    "ALTER TABLE tours_tour ADD COLUMN IF NOT EXISTS hotels_ja text;",
    "ALTER TABLE bookings_inquiry DROP COLUMN IF EXISTS hotel_id CASCADE;",
    "ALTER TABLE reviews_review DROP COLUMN IF EXISTS hotel_id CASCADE;"
]

for sql in sqls:
    print(f"Executing: {sql}")
    try:
        cursor.execute(sql)
    except Exception as e:
        print(f"Error: {e}")

connection.commit()
print("Schema fix applied!")
