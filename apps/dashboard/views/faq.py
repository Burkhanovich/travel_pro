"""Dashboard CRUD views for FAQs."""

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.dashboard.autotranslate import autofill_translations
from apps.dashboard.mixins import AuditMixin, ManagerRequiredMixin
from apps.faq.models import FAQ


class FAQListView(ManagerRequiredMixin, ListView):
    model = FAQ
    template_name = "dashboard/faq/list.html"
    context_object_name = "faqs"
    paginate_by = 20

    def get_queryset(self):
        qs = FAQ.objects.all().order_by("order", "-created_at")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(question__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class FAQCreateView(AuditMixin, ManagerRequiredMixin, CreateView):
    model = FAQ
    template_name = "dashboard/faq/form.html"
    success_url = reverse_lazy("dashboard:faq_list")
    fields = ["question", "answer", "order"]

    def form_valid(self, form):
        response = super().form_valid(form)
        autofill_translations(self.object)
        self.log_action("CREATE", "FAQ", self.object.pk)
        messages.success(self.request, gettext("FAQ created."))
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = _("Create FAQ")
        return ctx


class FAQEditView(AuditMixin, ManagerRequiredMixin, UpdateView):
    model = FAQ
    template_name = "dashboard/faq/form.html"
    success_url = reverse_lazy("dashboard:faq_list")
    fields = ["question", "answer", "order"]

    def form_valid(self, form):
        response = super().form_valid(form)
        autofill_translations(self.object)
        self.log_action("UPDATE", "FAQ", self.object.pk)
        messages.success(self.request, gettext("FAQ updated."))
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = _("Edit FAQ")
        return ctx


class FAQDeleteView(AuditMixin, ManagerRequiredMixin, DeleteView):
    model = FAQ
    success_url = reverse_lazy("dashboard:faq_list")
    template_name = "dashboard/confirm_delete.html"

    def form_valid(self, form):
        self.log_action("DELETE", "FAQ", self.object.pk)
        messages.success(self.request, gettext("FAQ deleted."))
        return super().form_valid(form)
