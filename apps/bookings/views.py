"""
Booking views: multi-step booking form and generic inquiry form.

Rate-limited to 5 submissions per hour per IP.
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from django_ratelimit.decorators import ratelimit

from apps.tours.models import Tour

from .forms import BookingForm, InquiryForm
from .models import Inquiry
from .tasks import send_booking_confirmation, send_admin_notification


class BookingFormView(FormView):
    """
    Multi-step tour booking form.

    Steps: 1 tour/departure → 2 personal info → 3 confirmation.
    Rate-limited: 5 submissions per hour per IP.
    """

    template_name = "tours/booking.html"
    form_class = BookingForm

    @ratelimit(key="ip", rate="5/h", method="POST", block=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        tour_slug = self.kwargs.get("slug") or self.request.GET.get("tour")
        if tour_slug:
            try:
                tour = Tour.objects.get(slug=tour_slug, is_active=True)
                initial["tour"] = tour.pk
            except Tour.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        if slug:
            ctx["tour"] = get_object_or_404(Tour, slug=slug, is_active=True)
        ctx["steps"] = [
            (1, _("Tour Details")),
            (2, _("Your Info")),
            (3, _("Confirmation")),
        ]
        ctx["current_step"] = 2
        return ctx

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        inquiry.source = "web"
        inquiry.created_ip = self._get_client_ip()
        inquiry.save()

        # Fire async email tasks
        send_booking_confirmation.delay(inquiry.pk)
        send_admin_notification.delay(inquiry.pk)

        return redirect("bookings:confirmation", pk=inquiry.pk)

    def _get_client_ip(self) -> str:
        x_fwd = self.request.META.get("HTTP_X_FORWARDED_FOR")
        return x_fwd.split(",")[0] if x_fwd else self.request.META.get("REMOTE_ADDR", "")


class BookingConfirmationView(TemplateView):
    """Show booking confirmation with reference number."""

    template_name = "bookings/confirmation.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["inquiry"] = get_object_or_404(Inquiry, pk=self.kwargs["pk"])
        return ctx


class InquiryFormView(FormView):
    """Generic inquiry / contact form for custom trip requests."""

    template_name = "bookings/inquiry.html"
    form_class = InquiryForm

    @ratelimit(key="ip", rate="5/h", method="POST", block=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        inquiry = form.save(commit=False)
        inquiry.source = "web"
        x_fwd = self.request.META.get("HTTP_X_FORWARDED_FOR")
        inquiry.created_ip = x_fwd.split(",")[0] if x_fwd else self.request.META.get("REMOTE_ADDR", "")
        inquiry.save()
        send_admin_notification.delay(inquiry.pk)
        messages.success(self.request, _("Thank you! We'll be in touch within 24 hours."))
        return redirect("bookings:inquiry")
