"""MICE corporate package views."""

from django.views.generic import DetailView, ListView

from .models import CorporatePackage


class MICEListView(ListView):
    """Grid listing of corporate travel packages."""

    model = CorporatePackage
    template_name = "mice/list.html"
    context_object_name = "packages"

    def get_queryset(self):
        return (
            CorporatePackage.objects.filter(is_active=True)
            .prefetch_related("featured_destinations")
            .order_by("order")
        )


class MICEDetailView(DetailView):
    """Full detail page for a corporate package."""

    model = CorporatePackage
    template_name = "mice/detail.html"
    context_object_name = "package"
    slug_field = "slug"

    def get_queryset(self):
        return CorporatePackage.objects.filter(is_active=True).prefetch_related("featured_destinations")
