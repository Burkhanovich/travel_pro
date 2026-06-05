"""MICE URL patterns."""

from django.urls import path

from .views import MICEDetailView, MICEListView

app_name = "mice"

urlpatterns = [
    path("", MICEListView.as_view(), name="list"),
    path("<slug:slug>/", MICEDetailView.as_view(), name="detail"),
]
