"""
MICE (Meetings, Incentives, Conferences, Exhibitions) models.

Corporate travel packages targeted at business clients.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import OrderedMixin, PublishableMixin, SEOMixin, TimeStampedModel


class CorporatePackage(TimeStampedModel, SEOMixin, PublishableMixin, OrderedMixin):
    """A MICE / corporate travel package."""

    PACKAGE_TYPE_CHOICES = [
        ("conference", _("Conference")),
        ("incentive", _("Incentive Trip")),
        ("exhibition", _("Exhibition")),
        ("team_building", _("Team Building")),
        ("retreat", _("Corporate Retreat")),
        ("product_launch", _("Product Launch")),
    ]

    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, blank=True)
    package_type = models.CharField(
        _("Package type"), max_length=20, choices=PACKAGE_TYPE_CHOICES, default="conference"
    )
    cover_image = models.ImageField(_("Cover image"), upload_to="mice/covers/", blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    includes = models.TextField(_("Package includes"), blank=True)
    min_participants = models.PositiveSmallIntegerField(_("Min participants"), default=10)
    max_participants = models.PositiveSmallIntegerField(_("Max participants"), default=500)
    price_per_person = models.DecimalField(
        _("Price per person (from)"), max_digits=10, decimal_places=2, default=0
    )
    featured_destinations = models.ManyToManyField(
        "destinations.Country",
        related_name="mice_packages",
        verbose_name=_("Featured destinations"),
        blank=True,
    )
    duration_days = models.PositiveSmallIntegerField(_("Duration (days)"), default=3)

    class Meta(OrderedMixin.Meta):
        verbose_name = _("Corporate package")
        verbose_name_plural = _("Corporate packages")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("mice:detail", kwargs={"slug": self.slug})
