"""Proxy model giving Uzbek (domestic) cities their own admin section.

Shares the destinations.City table — no new table is created. It exists so the
admin gets a separate "Ichki Turlar" section for managing the cities that
domestic multi-city tours are built from.
"""

from apps.destinations.models import City


class DomesticCity(City):
    class Meta:
        proxy = True
        verbose_name = "Shahar (Ichki Tur)"
        verbose_name_plural = "Shaharlar (Ichki Tur)"
