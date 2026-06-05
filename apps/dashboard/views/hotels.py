"""Dashboard CRUD views for Hotels."""

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.dashboard.mixins import AuditMixin, ManagerRequiredMixin
from apps.hotels.models import Hotel


class HotelListView(ManagerRequiredMixin, ListView):
    model = Hotel
    template_name = "dashboard/hotels/list.html"
    context_object_name = "hotels"
    paginate_by = 20

    def get_queryset(self):
        qs = Hotel.objects.select_related("city__country").order_by("-created_at")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class HotelCreateView(AuditMixin, ManagerRequiredMixin, CreateView):
    model = Hotel
    template_name = "dashboard/hotels/form.html"
    success_url = reverse_lazy("dashboard:hotels_list")
    fields = [
        "name", "city", "category", "stars", "cover_image",
        "address", "latitude", "longitude", "phone", "email",
        "website", "description", "amenities",
        "check_in_time", "check_out_time", "price_from",
        "is_active", "order",
    ]

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action("CREATE", "Hotel", self.object.pk)
        messages.success(self.request, f"Hotel '{self.object.name}' created.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Create Hotel"
        return ctx


class HotelEditView(AuditMixin, ManagerRequiredMixin, UpdateView):
    model = Hotel
    template_name = "dashboard/hotels/form.html"
    success_url = reverse_lazy("dashboard:hotels_list")
    fields = [
        "name", "city", "category", "stars", "cover_image",
        "address", "latitude", "longitude", "phone", "email",
        "website", "description", "amenities",
        "check_in_time", "check_out_time", "price_from",
        "is_active", "order",
    ]

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action("UPDATE", "Hotel", self.object.pk)
        messages.success(self.request, f"Hotel '{self.object.name}' updated.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = f"Edit: {self.object.name}"
        return ctx


class HotelDeleteView(AuditMixin, ManagerRequiredMixin, DeleteView):
    model = Hotel
    success_url = reverse_lazy("dashboard:hotels_list")

    def form_valid(self, form):
        self.log_action("DELETE", "Hotel", self.object.pk)
        messages.success(self.request, f"Hotel '{self.object.name}' deleted.")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
