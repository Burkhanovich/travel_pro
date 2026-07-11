from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from .models import FAQ


@method_decorator(cache_page(60 * 5), name="dispatch")
class FAQListView(ListView):
    model = FAQ
    template_name = "faq/list.html"
    context_object_name = "faqs"

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by("order", "created_at")
