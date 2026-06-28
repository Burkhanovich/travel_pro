"""Dashboard forms."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from apps.destinations.models import City, Country
from apps.tours.models import Tour, TourStop

User = get_user_model()

# Domestic ("Ichki Turlar") tours are built from Uzbek cities. Matched by name
# so the link survives slug/id changes (mirrors apps.ichki_turlar.admin).
DOMESTIC_COUNTRY = "Uzbek"

ROLE_CHOICES = [
    ("user", _("User — public site only")),
    ("operator", _("Operator — bookings & reviews")),
    ("manager", _("Manager — full content management")),
    ("superuser", _("Superuser — full access")),
]


class UserCreateForm(forms.Form):
    """Create a new account from the dashboard and assign a role.

    The site logs in by email, so the email doubles as the username. Role is
    applied separately (see ``apply_role``) since it maps to flags/groups
    rather than model fields.
    """

    email = forms.EmailField(label=_("Email"))
    first_name = forms.CharField(label=_("First name"), max_length=150, required=False)
    last_name = forms.CharField(label=_("Last name"), max_length=150, required=False)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, min_length=8)
    role = forms.ChoiceField(label=_("Role"), choices=ROLE_CHOICES, initial="user")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(
            username__iexact=email
        ).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def save(self):
        data = self.cleaned_data
        user = User(
            username=data["email"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.set_password(data["password"])
        user.save()
        return user


class UserEditForm(forms.ModelForm):
    """Edit an existing account's details, role and (optionally) password.

    Email doubles as the login username, so the two are kept in sync. Password
    is only changed when a new value is supplied.
    """

    role = forms.ChoiceField(label=_("Role"), choices=ROLE_CHOICES)
    password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        required=False,
        min_length=8,
        help_text=_("Leave blank to keep the current password."),
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "is_active"]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "is_active": _("Active (can log in)"),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        clash = (
            User.objects.filter(email__iexact=email)
            | User.objects.filter(username__iexact=email)
        ).exclude(pk=self.instance.pk)
        if clash.exists():
            raise forms.ValidationError(_("Another user with this email already exists."))
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class IchkiTurForm(forms.ModelForm):
    """Create/edit a domestic multi-city tour ("Ichki Tur").

    The itinerary stops (which make it multi-city) are handled by the
    ``TourStopFormSet`` alongside this form.
    """

    class Meta:
        model = Tour
        # Difficulty is intentionally omitted: domestic city tours don't need a
        # difficulty rating (it stays at the model default).
        fields = [
            "title", "category", "duration_days",
            "group_size_min", "group_size_max",
            "price_per_person", "price_currency", "discount_percent",
            "cover_image", "overview", "includes", "excludes",
            "important_notes", "is_active", "order",
        ]


class TourStopForm(forms.ModelForm):
    """A single itinerary stop, restricted to domestic (Uzbek) cities."""

    class Meta:
        model = TourStop
        fields = ["city", "order", "nights"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.filter(
            country__name__icontains=DOMESTIC_COUNTRY
        ).order_by("name")


# At least two stops are required — that is what makes a tour "Ichki Turlar".
TourStopFormSet = inlineformset_factory(
    Tour,
    TourStop,
    form=TourStopForm,
    extra=2,
    can_delete=True,
    min_num=2,
    validate_min=True,
)


class DomesticCityForm(forms.ModelForm):
    """Create/edit a domestic (Uzbek) city used to build Ichki Tur routes.

    New cities are always attached to Uzbekistan, so the country isn't shown.
    """

    class Meta:
        model = City
        # is_featured and order are omitted: featured has no effect for cities,
        # and cities are simply listed alphabetically by name.
        fields = ["name", "cover_image", "overview", "is_active"]

    def save(self, commit=True):
        city = super().save(commit=False)
        if city.country_id is None:
            city.country = Country.objects.filter(
                name__icontains=DOMESTIC_COUNTRY
            ).first()
        if commit:
            city.save()
        return city
