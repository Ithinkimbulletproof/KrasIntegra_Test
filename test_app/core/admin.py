from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "year_of_birth",
        "gender",
        "registration_date",
        "is_admin",
    )
    list_filter = ("gender", "is_admin")
    search_fields = ("full_name", "user__username")
    readonly_fields = ("registration_date",)
