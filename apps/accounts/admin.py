"""Admin configuration for user profiles."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"
    fields = ("avatar", "bio", "phone", "country", "city", "date_of_birth", "preferred_language", "newsletter_subscribed")


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "city", "preferred_language", "newsletter_subscribed")
    search_fields = ("user__username", "user__email", "country")
    list_filter = ("preferred_language", "newsletter_subscribed")
