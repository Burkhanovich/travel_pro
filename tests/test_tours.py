"""Tests for the tours app models and business logic."""

from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.urls import reverse

from apps.tours.models import Tour, TourDay, TourStop
from tests import factories as f

pytestmark = pytest.mark.django_db


class TestTourCategory:
    def test_str_and_slug(self):
        cat = f.make_tour_category(name="Adventure Trips")
        assert str(cat) == "Adventure Trips"
        assert cat.slug == "adventure-trips"

    def test_get_absolute_url(self):
        cat = f.make_tour_category(name="Beach", slug="beach")
        assert cat.get_absolute_url() == reverse("tours:list") + "?category=beach"


class TestTour:
    def test_str_and_slug(self):
        tour = f.make_tour(title="Silk Road Journey")
        assert str(tour) == "Silk Road Journey"
        assert tour.slug == "silk-road-journey"

    def test_get_absolute_url(self):
        tour = f.make_tour(title="Desert Tour", slug="desert-tour")
        assert tour.get_absolute_url() == reverse(
            "tours:detail", kwargs={"slug": "desert-tour"}
        )

    def test_discounted_price_no_discount(self):
        tour = f.make_tour(price_per_person=Decimal("1000"), discount_percent=0)
        assert tour.discounted_price == Decimal("1000")

    def test_discounted_price_with_discount(self):
        tour = f.make_tour(price_per_person=Decimal("1000"), discount_percent=25)
        assert tour.discounted_price == Decimal("750.00")

    def test_average_rating_no_reviews(self):
        tour = f.make_tour()
        assert tour.average_rating == 0.0

    def test_average_rating_only_approved(self):
        tour = f.make_tour()
        f.make_review(tour=tour, rating=4, status="approved")
        f.make_review(tour=tour, rating=2, status="approved")
        f.make_review(tour=tour, rating=5, status="pending")  # ignored
        assert tour.average_rating == 3.0

    def test_increment_views(self):
        tour = f.make_tour()
        assert tour.views_count == 0
        tour.increment_views()
        tour.refresh_from_db()
        assert tour.views_count == 1

    def test_is_multi_city_false_with_one_stop(self):
        tour = f.make_tour()
        f.make_tour_stop(tour, order=1)
        assert tour.is_multi_city is False

    def test_is_multi_city_true_with_two_stops(self):
        tour = f.make_tour()
        f.make_tour_stop(tour, order=1)
        f.make_tour_stop(tour, order=2)
        assert tour.is_multi_city is True


class TestTourStop:
    def test_str(self):
        tour = f.make_tour(title="Grand Tour")
        city = f.make_city(name="Bukhara")
        stop = f.make_tour_stop(tour, order=2, city=city)
        assert str(stop) == "Grand Tour – 2. Bukhara"

    def test_unique_order_per_tour(self):
        tour = f.make_tour()
        f.make_tour_stop(tour, order=1)
        with pytest.raises(IntegrityError):
            f.make_tour_stop(tour, order=1)


class TestTourDay:
    def test_str(self):
        tour = f.make_tour()
        day = TourDay.objects.create(
            tour=tour, day_number=3, title="Mountain Hike", description="..."
        )
        assert str(day) == "Day 3: Mountain Hike"

    def test_unique_day_number_per_tour(self):
        tour = f.make_tour()
        TourDay.objects.create(tour=tour, day_number=1, title="A", description="x")
        with pytest.raises(IntegrityError):
            TourDay.objects.create(tour=tour, day_number=1, title="B", description="y")


class TestTourDeparture:
    def test_str(self):
        tour = f.make_tour(title="Trek")
        dep = f.make_departure(tour=tour)
        assert str(dep).startswith("Trek – ")

    def test_seats_left(self):
        dep = f.make_departure(available_seats=20, booked_seats=5)
        assert dep.seats_left == 15

    def test_seats_left_never_negative(self):
        dep = f.make_departure(available_seats=5, booked_seats=10)
        assert dep.seats_left == 0

    def test_effective_price_uses_override(self):
        tour = f.make_tour(price_per_person=Decimal("1000"))
        dep = f.make_departure(tour=tour, price_override=Decimal("800"))
        assert dep.effective_price == Decimal("800")

    def test_effective_price_falls_back_to_discounted(self):
        tour = f.make_tour(price_per_person=Decimal("1000"), discount_percent=10)
        dep = f.make_departure(tour=tour, price_override=None)
        assert dep.effective_price == Decimal("900.0")

    def test_is_bookable_open_with_seats(self):
        dep = f.make_departure(status="open", available_seats=10, booked_seats=0)
        assert dep.is_bookable() is True

    def test_is_bookable_false_when_closed(self):
        dep = f.make_departure(status="closed", available_seats=10, booked_seats=0)
        assert dep.is_bookable() is False

    def test_is_bookable_false_when_full(self):
        dep = f.make_departure(status="open", available_seats=10, booked_seats=10)
        assert dep.is_bookable() is False
