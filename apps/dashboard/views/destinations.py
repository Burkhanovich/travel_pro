"""Dashboard CRUD views for Destinations (Countries & Cities)."""

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.dashboard.mixins import AuditMixin, ManagerRequiredMixin
from apps.destinations.models import City, Continent, Country


class DestinationListView(ManagerRequiredMixin, ListView):
    model = Country
    template_name = "dashboard/destinations/list.html"
    context_object_name = "countries"
    paginate_by = 30

    def get_queryset(self):
        qs = Country.objects.select_related("continent").order_by("name")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["continents"] = Continent.objects.all()
        return ctx


class CountryCreateView(AuditMixin, ManagerRequiredMixin, CreateView):
    model = Country
    template_name = "dashboard/destinations/country_form.html"
    success_url = reverse_lazy("dashboard:destinations_list")
    fields = ["name", "slug", "continent", "cover_image", "overview", "is_active"]

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action("CREATE", "Country", self.object.pk)
        messages.success(self.request, f"Country '{self.object.name}' created.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Add Country"
        return ctx


class CountryEditView(AuditMixin, ManagerRequiredMixin, UpdateView):
    model = Country
    template_name = "dashboard/destinations/country_form.html"
    success_url = reverse_lazy("dashboard:destinations_list")
    fields = ["name", "slug", "continent", "cover_image", "overview", "is_active"]

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action("UPDATE", "Country", self.object.pk)
        messages.success(self.request, f"Country '{self.object.name}' updated.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = f"Edit: {self.object.name}"
        return ctx


class CountryDeleteView(AuditMixin, ManagerRequiredMixin, DeleteView):
    model = Country
    success_url = reverse_lazy("dashboard:destinations_list")

    def form_valid(self, form):
        self.log_action("DELETE", "Country", self.object.pk)
        messages.success(self.request, f"Country '{self.object.name}' deleted.")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
