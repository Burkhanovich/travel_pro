"""Dashboard user management — superuser only."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import FormView

from apps.dashboard.forms import UserCreateForm
from apps.dashboard.mixins import AuditMixin, SuperuserRequiredMixin

User = get_user_model()

VALID_ROLES = {"superuser", "manager", "operator", "user"}


def apply_role(user, role: str) -> bool:
    """Set a user's staff/superuser flags and groups for the given role.

    Returns True if the role was recognised and applied, False otherwise.
    """
    if role == "superuser":
        user.is_staff = True
        user.is_superuser = True
        user.groups.clear()
    elif role == "manager":
        user.is_staff = True
        user.is_superuser = False
        user.groups.set(Group.objects.filter(name="Manager"))
    elif role == "operator":
        user.is_staff = True
        user.is_superuser = False
        user.groups.set(Group.objects.filter(name="Operator"))
    elif role == "user":
        user.is_staff = False
        user.is_superuser = False
        user.groups.clear()
    else:
        return False
    user.save(update_fields=["is_staff", "is_superuser"])
    return True


class UserListView(SuperuserRequiredMixin, ListView):
    model = User
    template_name = "dashboard/users/list.html"
    context_object_name = "users"
    paginate_by = 30

    def get_queryset(self):
        qs = User.objects.prefetch_related("groups").order_by("-date_joined")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(email__icontains=q) | qs.filter(
                first_name__icontains=q
            ) | qs.filter(last_name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["groups"] = Group.objects.all()
        return ctx


class UserCreateView(AuditMixin, SuperuserRequiredMixin, FormView):
    """Create a new account and assign its role — superuser only."""

    form_class = UserCreateForm
    template_name = "dashboard/users/form.html"
    success_url = reverse_lazy("dashboard:users_list")

    def form_valid(self, form):
        user = form.save()
        apply_role(user, form.cleaned_data["role"])
        self.log_action("CREATE", "User", user.pk)
        messages.success(
            self.request,
            f"User {user.email} created with role '{form.cleaned_data['role']}'.",
        )
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = "Create User"
        return ctx


class UserRoleUpdateView(AuditMixin, SuperuserRequiredMixin, View):
    """Update a user's role (groups + is_staff flag) via POST."""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # Prevent demoting yourself
        if user == request.user:
            messages.error(request, "You cannot change your own role.")
            return redirect("dashboard:users_list")

        role = request.POST.get("role", "")
        if not apply_role(user, role):
            messages.error(request, "Unknown role.")
            return redirect("dashboard:users_list")

        self.log_action("ROLE_CHANGE", "User", pk)
        messages.success(request, f"Role for {user.email} updated to '{role}'.")
        return redirect("dashboard:users_list")
