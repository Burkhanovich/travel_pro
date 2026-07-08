"""Tests for the reviews app."""

import pytest
from django.urls import reverse

from apps.reviews.models import Review
from tests import factories as f

pytestmark = pytest.mark.django_db


class TestReview:
    def test_str_with_guest(self):
        review = f.make_review(guest_name="Bob", rating=3, title="Nice")
        assert str(review) == "Bob – ★★★ – Nice"

    def test_str_with_user(self):
        user = f.make_user(first_name="Jane", last_name="Doe")
        review = f.make_review(user=user, rating=5, title="Excellent journey")
        assert "Jane Doe" in str(review)

    def test_reviewer_name_user_full_name(self):
        user = f.make_user(first_name="Jane", last_name="Doe")
        review = f.make_review(user=user)
        assert review.reviewer_name == "Jane Doe"

    def test_reviewer_name_user_email_fallback(self):
        user = f.make_user(first_name="", last_name="", email="x@y.com")
        review = f.make_review(user=user)
        assert review.reviewer_name == "x@y.com"

    def test_reviewer_name_guest(self):
        review = f.make_review(guest_name="Charlie")
        assert review.reviewer_name == "Charlie"

    def test_reviewer_name_anonymous(self):
        review = f.make_review(guest_name="")
        assert review.reviewer_name == "Anonymous"

    def test_star_ranges(self):
        review = f.make_review(rating=4)
        assert list(review.star_range) == [0, 1, 2, 3]
        assert list(review.empty_star_range) == [0]

    def test_approve(self):
        review = f.make_review(status="pending")
        review.approve()
        review.refresh_from_db()
        assert review.status == "approved"

    def test_reject(self):
        review = f.make_review(status="pending")
        review.reject()
        review.refresh_from_db()
        assert review.status == "rejected"

    def test_default_status_pending(self):
        review = f.make_review()
        assert review.status == "pending"


class TestReviewSubmission:
    """The public "Write a Review" form creates pending reviews."""

    def _payload(self, **overrides):
        data = {
            "review_type": "general",
            "rating": 5,
            "title": "Wonderful",
            "body": "Had a fantastic time.",
            "guest_name": "Traveler",
            "guest_country": "France",
        }
        data.update(overrides)
        return data

    def test_get_list_page_shows_form(self, client):
        resp = client.get(reverse("reviews:list"))
        assert resp.status_code == 200
        assert "form" in resp.context
        assert 'action="{}"'.format(reverse("reviews:create")) in resp.content.decode()

    def test_submit_creates_pending_review(self, client):
        resp = client.post(reverse("reviews:create"), self._payload())
        assert resp.status_code == 302
        review = Review.objects.get(title="Wonderful")
        assert review.status == "pending"
        assert review.guest_name == "Traveler"

    def test_pending_review_not_public_until_approved(self, client):
        client.post(reverse("reviews:create"), self._payload(title="Hidden"))
        resp = client.get(reverse("reviews:list"))
        assert "Hidden" not in resp.content.decode()

        review = Review.objects.get(title="Hidden")
        review.approve()
        resp = client.get(reverse("reviews:list"))
        assert "Hidden" in resp.content.decode()

    def test_tour_review_requires_tour(self, client):
        # review_type=tour but no tour chosen → invalid, re-renders with errors.
        resp = client.post(
            reverse("reviews:create"),
            self._payload(review_type="tour"),
        )
        assert resp.status_code == 200
        assert not Review.objects.filter(title="Wonderful").exists()
        assert resp.context["form"].errors

    def test_tour_review_with_tour_succeeds(self, client):
        tour = f.make_tour(title="Silk Road")
        resp = client.post(
            reverse("reviews:create"),
            self._payload(review_type="tour", tour=tour.pk),
        )
        assert resp.status_code == 302
        assert Review.objects.filter(tour=tour, status="pending").exists()


class TestDashboardReviewDelete:
    """Managers can permanently delete a review from the dashboard."""

    def test_delete_removes_review(self, client):
        manager = f.make_user(is_staff=True, is_superuser=True)
        client.force_login(manager)
        review = f.make_review(title="To Delete", status="approved")

        resp = client.post(
            reverse("dashboard:reviews_list"),
            {"pk": review.pk, "action": "delete"},
        )
        assert resp.status_code == 302
        assert not Review.objects.filter(pk=review.pk).exists()
