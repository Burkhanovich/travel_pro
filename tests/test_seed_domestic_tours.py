"""Tests for the ``seed_domestic_tours`` management command."""

import pytest
from django.core.management import call_command
from django.db.models import Count

from apps.destinations.models import City, Country
from apps.tours.models import Tour
from tests import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def uzbekistan():
    return f.make_country(name="Uzbekistan")


def _multi_city_count():
    return Tour.objects.annotate(n=Count("stops")).filter(n__gt=1).count()


def test_creates_multi_city_tours(uzbekistan):
    call_command("seed_domestic_tours", verbosity=0)
    assert _multi_city_count() == 5
    # Every seeded tour has an ordered, multi-stop itinerary.
    golden = Tour.objects.get(slug="golden-road-of-uzbekistan")
    assert list(golden.stops.values_list("order", flat=True)) == [1, 2, 3, 4]
    # Missing Uzbek cities were created and attached to Uzbekistan.
    assert City.objects.filter(name="Bukhara", country=uzbekistan).exists()


def test_is_idempotent(uzbekistan):
    call_command("seed_domestic_tours", verbosity=0)
    tours_after_first = Tour.objects.count()
    cities_after_first = City.objects.count()

    call_command("seed_domestic_tours", verbosity=0)
    assert Tour.objects.count() == tours_after_first
    assert City.objects.count() == cities_after_first


def test_aborts_without_uzbekistan():
    # No Uzbekistan country in the DB → nothing is created.
    assert not Country.objects.filter(name_en__icontains="Uzbek").exists()
    call_command("seed_domestic_tours", verbosity=0)
    assert Tour.objects.count() == 0
