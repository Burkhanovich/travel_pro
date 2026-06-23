"""Dashboard forms."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

ROLE_CHOICES = [
    ("user", "User — public site only"),
    ("operator", "Operator — bookings & reviews"),
    ("manager", "Manager — full content management"),
    ("superuser", "Superuser — full access"),
]


class UserCreateForm(forms.Form):
    """Create a new account from the dashboard and assign a role.

    The site logs in by email, so the email doubles as the username. Role is
    applied separately (see ``apply_role``) since it maps to flags/groups
    rather than model fields.
    """

    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name", max_length=150, required=False)
    last_name = forms.CharField(label="Last name", max_length=150, required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8)
    role = forms.ChoiceField(label="Role", choices=ROLE_CHOICES, initial="user")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(
            username__iexact=email
        ).exists():
            raise forms.ValidationError("A user with this email already exists.")
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
