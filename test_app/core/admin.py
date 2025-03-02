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
        "registered_by",
    )
    list_filter = ("gender", "is_admin")
    search_fields = ("full_name", "user__username")
    readonly_fields = ("registration_date",)

    def save_model(self, request, obj, form, change):
        if obj.user:
            obj.user.is_staff = obj.is_admin
            obj.user.save()
        super().save_model(request, obj, form, change)
