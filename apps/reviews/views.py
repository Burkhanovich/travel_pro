"""Review list view with filtering by type and rating."""

from django.views.generic import ListView

from .models import Review


REVIEW_TYPE_CHOICES = [
    ("tour", "Tour Reviews"),
    ("hotel", "Hotel Reviews"),
    ("general", "General Reviews"),
]


class ReviewListView(ListView):
    """Paginated list of approved reviews with optional type/rating filters."""

    model = Review
    template_name = "reviews/list.html"
    context_object_name = "reviews"
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Review.objects.filter(status="approved")
            .select_related("user", "tour", "hotel")
            .order_by("-created_at")
        )
        review_type = self.request.GET.get("type")
        if review_type in ("tour", "hotel", "general"):
            qs = qs.filter(review_type=review_type)

        rating = self.request.GET.get("rating")
        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            qs = qs.filter(rating=int(rating))

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_type"] = self.request.GET.get("type", "")
        ctx["current_rating"] = self.request.GET.get("rating", "")
        ctx["review_types"] = REVIEW_TYPE_CHOICES
        return ctx
