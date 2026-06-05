"""modeltranslation registration for MICE models."""

from modeltranslation.translator import TranslationOptions, register

from .models import CorporatePackage


@register(CorporatePackage)
class CorporatePackageTranslationOptions(TranslationOptions):
    fields = ("title", "description", "includes", "seo_title", "seo_description")
