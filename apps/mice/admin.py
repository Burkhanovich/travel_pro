"""Admin configuration for MICE corporate packages."""

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import CorporatePackage


@admin.register(CorporatePackage)
class CorporatePackageAdmin(TranslationAdmin):
    list_display = ("title", "package_type", "min_participants", "max_participants", "price_per_person", "is_featured", "is_active", "order")
    list_filter = ("package_type", "is_featured", "is_active")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured", "is_active", "order")
    filter_horizontal = ("featured_destinations",)
