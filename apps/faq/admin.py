from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("question", "answer")
