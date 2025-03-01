from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_list, name="profile_list"),
    path("profile/<int:pk>/", views.profile_detail, name="profile_detail"),
    path("profile/create/", views.profile_create, name="profile_create"),
    path("profile/<int:pk>/edit/", views.profile_edit, name="profile_edit"),
    path("profile/<int:pk>/delete/", views.profile_delete, name="profile_delete"),
    path("accounts/register/", views.register, name="register"),
]
