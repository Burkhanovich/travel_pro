from modeltranslation.translator import TranslationOptions, register
from .models import FAQ


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")
