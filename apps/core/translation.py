"""modeltranslation registration for core models."""

from modeltranslation.translator import TranslationOptions, register
from .models import ContactSettings


@register(ContactSettings)
class ContactSettingsTranslationOptions(TranslationOptions):
    fields = ("address", "working_hours")
