"""Dashboard URL configuration."""

from django.urls import path

from apps.dashboard.views.articles import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleEditView,
    ArticleListView,
)
from apps.dashboard.views.bookings import (
    BookingDetailView,
    BookingListView,
    booking_export_csv,
)
from apps.dashboard.views.destinations import (
    CountryCreateView,
    CountryDeleteView,
    CountryEditView,
    DestinationListView,
)
from apps.dashboard.views.home import DashboardHomeView, dashboard_stats_api
from apps.dashboard.views.hotels import (
    HotelCreateView,
    HotelDeleteView,
    HotelEditView,
    HotelListView,
)
from apps.dashboard.views.reviews import ReviewListView
from apps.dashboard.views.tours import (
    TourCreateView,
    TourDeleteView,
    TourEditView,
    TourListView,
)
from apps.dashboard.views.users import UserListView, UserRoleUpdateView

app_name = "dashboard"

urlpatterns = [
    # Home
    path("", DashboardHomeView.as_view(), name="home"),
    path("api/stats/", dashboard_stats_api, name="stats_api"),

    # Tours
    path("tours/", TourListView.as_view(), name="tours_list"),
    path("tours/create/", TourCreateView.as_view(), name="tours_create"),
    path("tours/<int:pk>/edit/", TourEditView.as_view(), name="tours_edit"),
    path("tours/<int:pk>/delete/", TourDeleteView.as_view(), name="tours_delete"),

    # Hotels
    path("hotels/", HotelListView.as_view(), name="hotels_list"),
    path("hotels/create/", HotelCreateView.as_view(), name="hotels_create"),
    path("hotels/<int:pk>/edit/", HotelEditView.as_view(), name="hotels_edit"),
    path("hotels/<int:pk>/delete/", HotelDeleteView.as_view(), name="hotels_delete"),

    # Destinations
    path("destinations/", DestinationListView.as_view(), name="destinations_list"),
    path("destinations/create/", CountryCreateView.as_view(), name="destinations_create"),
    path("destinations/<int:pk>/edit/", CountryEditView.as_view(), name="destinations_edit"),
    path("destinations/<int:pk>/delete/", CountryDeleteView.as_view(), name="destinations_delete"),

    # Bookings
    path("bookings/", BookingListView.as_view(), name="bookings_list"),
    path("bookings/export/", booking_export_csv, name="bookings_export"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking_detail"),

    # Articles
    path("articles/", ArticleListView.as_view(), name="articles_list"),
    path("articles/create/", ArticleCreateView.as_view(), name="articles_create"),
    path("articles/<int:pk>/edit/", ArticleEditView.as_view(), name="articles_edit"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="articles_delete"),

    # Reviews
    path("reviews/", ReviewListView.as_view(), name="reviews_list"),

    # Users
    path("users/", UserListView.as_view(), name="users_list"),
    path("users/<int:pk>/role/", UserRoleUpdateView.as_view(), name="users_role"),
]
