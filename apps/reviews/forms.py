"""Public-facing review submission form."""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Review


class ReviewCreateForm(forms.ModelForm):
    """Let visitors submit a review from the public reviews page.

    ``tour`` and ``hotel`` stay optional here — a general review needs neither,
    and a tour/hotel review only fills the one that matches ``review_type``.
    Submitted reviews always start in the ``pending`` moderation queue (set by
    the view, never trusted from the form).
    """

    class Meta:
        model = Review
        fields = [
            "review_type",
            "tour",
            "hotel",
            "rating",
            "title",
            "body",
            "guest_name",
            "guest_country",
            "travel_date",
        ]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} ★") for i in range(5, 0, -1)]),
            "body": forms.Textarea(attrs={"rows": 4}),
            "travel_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "guest_name": _("Your name"),
            "guest_country": _("Country"),
            "body": _("Your review"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tour"].required = False
        self.fields["hotel"].required = False
        self.fields["guest_name"].required = True
        # A consistent, compact look for every widget.
        base = (
            "w-full border border-gray-300 rounded-lg px-3 py-2 text-sm "
            "focus:ring-primary focus:border-primary"
        )
        for name, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} {base}".strip()

    def clean(self):
        cleaned = super().clean()
        review_type = cleaned.get("review_type")
        if review_type == "tour" and not cleaned.get("tour"):
            self.add_error("tour", _("Please choose the tour you are reviewing."))
        elif review_type == "hotel" and not cleaned.get("hotel"):
            self.add_error("hotel", _("Please choose the hotel you are reviewing."))
        return cleaned
