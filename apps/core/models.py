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


class HeroSlide(TimeStampedModel, OrderedMixin):
    """A background image for a page's rotating hero slideshow.

    Managed from the dashboard so staff can upload/replace the rotating
    background images without code changes.
    """

    PAGE_CHOICES = [
        ("ichki_turlar", _("Domestic Tours")),
        ("home", _("Home")),
        ("tours", _("Tours")),
        ("destinations", _("Destinations")),
        ("hotels", _("Hotels")),
        ("guides", _("Guides")),
    ]

    page = models.CharField(
        _("Page"), max_length=32, choices=PAGE_CHOICES,
        default="ichki_turlar", db_index=True,
        help_text=_("Which page's hero slideshow this image belongs to."),
    )
    image = models.ImageField(_("Image"), upload_to="hero_slides/")
    alt = models.CharField(_("Alt text"), max_length=200, blank=True)
    is_active = models.BooleanField(_("Active"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Hero slide")
        verbose_name_plural = _("Hero slides")
        ordering = ["page", "order", "-created_at"]

    def __str__(self) -> str:
        return f"{self.get_page_display()} — {self.alt or self.image.name}"


class ContactSettings(TimeStampedModel):
    """
    Site-wide contact information and social links managed from the admin.
    """
    phone = models.CharField(_("Phone"), max_length=50, default="+998919917101")
    email = models.EmailField(_("Email"), default="burkhanov1c@gmail.com")
    address = models.CharField(_("Address"), max_length=255, default="Navoiy viloyati, Navoiy shahri, Jasorat 29-36")
    working_hours = models.CharField(_("Working hours"), max_length=255, default="Dushanba–Shanba, 9:00–18:00")
    
    # Social links
    youtube = models.URLField(_("YouTube"), blank=True, default="https://youtube.com/@Unituruz")
    instagram = models.URLField(_("Instagram"), blank=True, default="https://instagram.com/unitouruz")
    telegram = models.URLField(_("Telegram"), blank=True, default="https://t.me/unituruz")
    facebook = models.URLField(_("Facebook"), blank=True, default="https://facebook.com/unituruz")
    
    # Coordinates (for the map on the contact page)
    latitude = models.FloatField(_("Latitude"), default=40.0844, null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), default=65.3792, null=True, blank=True)

    class Meta:
        verbose_name = _("Contact Settings")
        verbose_name_plural = _("Contact Settings")

    def __str__(self) -> str:
        return f"Site Contact Settings ({self.email})"

