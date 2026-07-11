from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FAQConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.faq"
    verbose_name = _("FAQ")
