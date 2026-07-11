from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import OrderedMixin, TimeStampedModel


class FAQ(TimeStampedModel, OrderedMixin):
    """
    Frequently Asked Questions (FAQ) model.
    """
    question = models.CharField(_("Question"), max_length=255)
    answer = models.TextField(_("Answer"))
    is_active = models.BooleanField(_("Active"), default=True, db_index=True)

    class Meta(OrderedMixin.Meta):
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self) -> str:
        return self.question
