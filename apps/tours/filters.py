"""django-filter FilterSet for Tour list view."""

import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.destinations.models import Country

from .models import Tour, TourCategory


class TourFilter(django_filters.FilterSet):
    """Filter tours by category, destination, duration, price, difficulty, and departure month."""

    category = django_filters.ModelChoiceFilter(
        queryset=TourCategory.objects.all(),
        label=_("Category"),
        empty_label=_("All categories"),
    )
    destination = django_filters.ModelMultipleChoiceFilter(
        field_name="destinations",
        queryset=Country.objects.filter(is_active=True),
        label=_("Destination"),
        widget=forms.CheckboxSelectMultiple,
    )
    min_price = django_filters.NumberFilter(field_name="price_per_person", lookup_expr="gte", label=_("Min price"))
    max_price = django_filters.NumberFilter(field_name="price_per_person", lookup_expr="lte", label=_("Max price"))
    min_duration = django_filters.NumberFilter(field_name="duration_days", lookup_expr="gte", label=_("Min days"))
    max_duration = django_filters.NumberFilter(field_name="duration_days", lookup_expr="lte", label=_("Max days"))
    difficulty = django_filters.ChoiceFilter(
        choices=[("", _("Any difficulty"))] + Tour.DIFFICULTY_CHOICES,
        label=_("Difficulty"),
    )
    departure_month = django_filters.NumberFilter(
        field_name="departures__departure_date__month",
        label=_("Departure month"),
        distinct=True,
    )

    class Meta:
        model = Tour
        fields = ["category", "destination", "difficulty"]
