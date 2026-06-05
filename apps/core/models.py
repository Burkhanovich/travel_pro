"""Core abstract base models shared across all apps."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Abstract base providing created_at / updated_at timestamps."""

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SEOMixin(models.Model):
    """Abstract mixin adding SEO meta fields."""

    seo_title = models.CharField(_("SEO title"), max_length=70, blank=True)
    seo_description = models.CharField(_("SEO description"), max_length=160, blank=True)

    class Meta:
        abstract = True


class PublishableMixin(models.Model):
    """Abstract mixin adding is_active / is_featured flags."""

    is_active = models.BooleanField(_("Active"), default=True, db_index=True)
    is_featured = models.BooleanField(_("Featured"), default=False, db_index=True)

    class Meta:
        abstract = True


class OrderedMixin(models.Model):
    """Abstract mixin adding order field for manual sorting."""

    order = models.PositiveSmallIntegerField(_("Display order"), default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["order"]
