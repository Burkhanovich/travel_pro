"""Dashboard access middleware — blocks non-staff from /dashboard/."""

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect


class DashboardAccessMiddleware:
    """Redirect unauthenticated users and block non-staff from /dashboard/."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/dashboard/"):
            if not request.user.is_authenticated:
                login_url = getattr(settings, "LOGIN_URL", "/accounts/login/")
                return redirect(f"{login_url}?next={request.path}")
            if not request.user.is_staff:
                raise Http404
        return self.get_response(request)
