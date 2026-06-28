"""Set a city's cover image from a URL.

Useful for replacing an auto-fetched placeholder with an accurate, properly
licensed photo (e.g. from Wikimedia Commons).

    python manage.py set_city_image "Samarkand" "https://upload.wikimedia.org/.../1600px-Registan.jpg"
"""

import ssl
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from apps.destinations.models import City


class Command(BaseCommand):
    help = "Download an image from a URL and set it as a city's cover image."

    def add_arguments(self, parser):
        parser.add_argument("city", help="City name (exact or partial match).")
        parser.add_argument("url", help="Image URL to download.")

    def handle(self, *args, **opts):
        name, url = opts["city"], opts["url"]

        matches = City.objects.filter(name__icontains=name)
        if not matches:
            raise CommandError(f"No city matching '{name}'.")
        if matches.count() > 1:
            exact = matches.filter(name__iexact=name)
            if exact.count() == 1:
                matches = exact
            else:
                raise CommandError(
                    f"'{name}' matches {matches.count()} cities: "
                    + ", ".join(matches.values_list("name", flat=True))
                )
        city = matches.first()

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(
            url, headers={"User-Agent": "TravelPro/1.0 (+https://unitur.uz; admin@travelpro.com)"}
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
                data = r.read()
        except Exception as exc:  # noqa: BLE001
            raise CommandError(f"Download failed: {exc}")

        if len(data) < 10_000:
            raise CommandError(f"Downloaded file too small ({len(data)} bytes).")

        city.cover_image.save(f"{slugify(city.name)}-cover.jpg", ContentFile(data), save=True)
        self.stdout.write(self.style.SUCCESS(
            f"{city.name}: cover image set ({len(data) // 1024} KB) → {city.cover_image.url}"
        ))
