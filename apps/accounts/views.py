"""Account views: user profile with booking history and saved tours."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.bookings.models import Inquiry


class UserProfileView(LoginRequiredMixin, TemplateView):
    """
    Authenticated user profile page.

    Shows booking history and saved tours.
    """

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        ctx["inquiries"] = (
            Inquiry.objects.filter(email=user.email)
            .select_related("tour", "hotel")
            .order_by("-created_at")[:20]
        )

        if hasattr(user, "profile"):
            ctx["saved_tours"] = user.profile.saved_tours.filter(is_active=True)[:12]
        else:
            ctx["saved_tours"] = []

        return ctx
