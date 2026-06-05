"""Dashboard CRUD views for Tours."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.dashboard.mixins import AuditMixin, ManagerRequiredMixin
from apps.tours.models import Tour, TourCategory


class TourListView(ManagerRequiredMixin, ListView):
    model = Tour
    template_name = "dashboard/tours/list.html"
    context_object_name = "tours"
    paginate_by = 20

    def get_queryset(self):
        qs = Tour.objects.select_related("category").order_by("-created_at")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(title__icontains=q)
        cat = self.request.GET.get("category", "")
        if cat:
            qs = qs.filter(category__slug=cat)
        status = self.request.GET.get("status", "")
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = TourCategory.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["selected_category"] = self.request.GET.get("category", "")
        ctx["selected_status"] = self.request.GET.get("status", "")
        return ctx


class TourCreateView(AuditMixin, ManagerRequiredMixin, CreateView):
    model = Tour
    template_name = "dashboard/tours/form.html"
    success_url = reverse_lazy("dashboard:tours_list")
    fields = [
        "title", "category", "destinations", "duration_days",
        "group_size_min", "group_size_max", "difficulty",
        "price_per_person", "price_currency", "discount_percent",
        "cover_image", "overview", "includes", "excludes",
        "important_notes", "is_active", "order",
    ]

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action("CREATE", "Tour", self.object.pk)
        messages.success(self.request, f"Tour '{self.object.title}' created.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Create Tour"
        ctx["categories"] = TourCategory.objects.all()
        return ctx


class TourEditView(AuditMixin, ManagerRequiredMixin, UpdateView):
    model = Tour
    template_name = "dashboard/tours/form.html"
    success_url = reverse_lazy("dashboard:tours_list")
    fields = [
        "title", "category", "destinations", "duration_days",
        "group_size_min", "group_size_max", "difficulty",
        "price_per_person", "price_currency", "discount_percent",
        "cover_image", "overview", "includes", "excludes",
        "important_notes", "is_active", "order",
    ]

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action("UPDATE", "Tour", self.object.pk)
        messages.success(self.request, f"Tour '{self.object.title}' updated.")
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = f"Edit: {self.object.title}"
        ctx["categories"] = TourCategory.objects.all()
        return ctx


class TourDeleteView(AuditMixin, ManagerRequiredMixin, DeleteView):
    model = Tour
    success_url = reverse_lazy("dashboard:tours_list")

    def form_valid(self, form):
        self.log_action("DELETE", "Tour", self.object.pk)
        messages.success(self.request, f"Tour '{self.object.title}' deleted.")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
