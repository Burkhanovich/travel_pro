"""Add a curated set of gallery photos to a city.

Fetches each landmark's lead image from Wikipedia (properly licensed), downsizes
it with Pillow, creates a CityImage with a caption + description, and machine-
translates those into every site language. Idempotent (skips captions already
present).

    python manage.py add_city_gallery "Samarkand"
"""

import io
import json
import ssl
import time
import urllib.parse
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from apps.destinations.models import City, CityImage

MAX_WIDTH = 1600
_UA = "TravelPro/1.0 (+https://unitur.uz; admin@unitur.uz)"

# city name (lowercase) -> list of (wikipedia_title, caption, description)
GALLERIES = {
    "samarkand": [
        ("Registan", "Registan Square",
         "The heart of ancient Samarkand — three grand madrasas (Ulugh Beg, Sher-Dor and Tilya-Kori) framing a majestic public square."),
        ("Shah-i-Zinda", "Shah-i-Zinda",
         "A breathtaking avenue of mausoleums adorned with some of the finest blue majolica tilework in the Islamic world."),
        ("Gur-e-Amir", "Gur-e-Amir Mausoleum",
         "The tomb of Amir Timur (Tamerlane), crowned by a fluted azure dome — a masterpiece of Timurid architecture."),
        ("Bibi-Khanym Mosque", "Bibi-Khanym Mosque",
         "Once one of the largest mosques of the medieval Islamic world, built by Timur after his campaign in India."),
        ("Ulugh Beg Observatory", "Ulugh Beg Observatory",
         "Remains of a 15th-century astronomical observatory built by the scholar-king Ulugh Beg."),
    ],
}


class Command(BaseCommand):
    help = "Add a curated Wikipedia-sourced photo gallery to a city."

    def add_arguments(self, parser):
        parser.add_argument("city", help="City name (exact or partial).")
        parser.add_argument("--no-translate", action="store_true")

    _ctx = None

    def ctx(self):
        if self._ctx is None:
            c = ssl.create_default_context()
            c.check_hostname = False
            c.verify_mode = ssl.CERT_NONE
            self._ctx = c
        return self._ctx

    def _get(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, context=self.ctx(), timeout=30) as r:
            return r.read()

    def _wiki_image_url(self, title):
        api = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"))
        data = json.loads(self._get(api))
        return (data.get("originalimage") or {}).get("source")

    def _download_resized(self, url):
        data = self._get(url)
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85, optimize=True)
            return buf.getvalue()
        except Exception:  # noqa: BLE001 - fall back to raw bytes
            return data

    def handle(self, *args, **opts):
        name = opts["city"]
        matches = City.objects.filter(name_en__icontains=name) or City.objects.filter(name__icontains=name)
        if not matches:
            raise CommandError(f"No city matching '{name}'.")
        city = matches.first()

        curated = GALLERIES.get(city.name_en.lower()) or GALLERIES.get(name.lower())
        if not curated:
            raise CommandError(
                f"No curated gallery defined for '{city.name_en}'. "
                f"Available: {', '.join(GALLERIES)}"
            )

        autofill = None
        if not opts["no_translate"]:
            from apps.dashboard.autotranslate import autofill_translations
            autofill = autofill_translations

        existing = set(city.images.values_list("caption_en", flat=True))
        start_order = (city.images.count() or 0)
        added = 0

        for i, (title, caption, description) in enumerate(curated):
            if caption in existing:
                self.stdout.write(f"  = {caption} (already present, skipped)")
                continue
            try:
                img_url = self._wiki_image_url(title)
                if not img_url:
                    self.stderr.write(self.style.WARNING(f"  ! {title}: no image on Wikipedia"))
                    continue
                data = self._download_resized(img_url)
                if len(data) < 10_000:
                    self.stderr.write(self.style.WARNING(f"  ! {title}: image too small"))
                    continue
                obj = CityImage(city=city, caption=caption, description=description,
                                order=start_order + i)
                obj.image.save(f"{slugify(city.name_en)}-{slugify(caption)}.jpg",
                               ContentFile(data), save=True)
                if autofill:
                    autofill(obj, source_lang="en", overwrite=False, force=True)
                added += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  + {caption} ({len(data)//1024} KB)"))
                time.sleep(0.3)
            except Exception as exc:  # noqa: BLE001
                self.stderr.write(self.style.WARNING(f"  ! {title}: {exc}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {added} gallery image(s) added to {city.name_en}."
        ))
