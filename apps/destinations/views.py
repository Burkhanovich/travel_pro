"""Destination views: continent/country listing, country detail, city detail."""

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from apps.tours.models import Tour

from .models import City, Continent, Country


class DestinationListView(ListView):
    """
    List all countries grouped by continent.

    Annotates each country with its active tour count.
    """

    model = Country
    template_name = "destinations/list.html"
    context_object_name = "countries"

    def get_queryset(self):
        return (
            Country.objects.filter(is_active=True)
            .select_related("continent")
            .annotate(num_tours=Count("tours", filter=Q(tours__is_active=True)))
            .order_by("continent__order", "order", "name")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["continents"] = Continent.objects.all().order_by("order")
        return ctx


class CountryDetailView(DetailView):
    """Country page showing cities, tours, and overview."""

    model = Country
    template_name = "destinations/country.html"
    context_object_name = "country"
    slug_field = "slug"

    def get_queryset(self):
        return Country.objects.filter(is_active=True).select_related("continent").prefetch_related("cities")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        country = self.object
        ctx["cities"] = country.cities.filter(is_active=True).order_by("order")
        ctx["tours"] = (
            Tour.objects.filter(destinations=country, is_active=True)
            .select_related("category")
            .order_by("order")[:8]
        )
        ctx["breadcrumbs"] = [
            {"name": "Destinations", "url": "/destinations/"},
            {"name": country.name, "url": None},
        ]
        return ctx


class CityDetailView(DetailView):
    """City page with attractions, hotels, and local tours."""

    model = City
    template_name = "destinations/city.html"
    context_object_name = "city"

    def get_object(self, queryset=None):
        country_slug = self.kwargs["country_slug"]
        city_slug = self.kwargs["city_slug"]
        return get_object_or_404(
            City.objects.select_related("country").prefetch_related("attractions", "hotels"),
            slug=city_slug,
            country__slug=country_slug,
            is_active=True,
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        city = self.object
        ctx["attractions"] = city.attractions.filter(is_active=True)
        ctx["hotels"] = city.hotels.filter(is_active=True).order_by("order")[:6]
        ctx["tours"] = (
            Tour.objects.filter(destinations__cities=city, is_active=True)
            .distinct()
            .select_related("category")[:6]
        )
        return ctx
