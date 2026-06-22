"""Tests for the reviews app."""

import pytest

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
