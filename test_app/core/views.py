from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import RegistrationForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView


class MyLogoutView(LogoutView):
    http_method_names = ["get", "post"]


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            year_of_birth = form.cleaned_data.get("year_of_birth")
            gender = form.cleaned_data.get("gender")
            photo = form.cleaned_data.get("photo")
            is_admin = form.cleaned_data.get("is_admin")
            if request.user.is_authenticated and request.user != user:
                reg_by = request.user.username
            else:
                reg_by = "сам"
            UserProfile.objects.create(
                user=user,
                full_name=full_name,
                year_of_birth=year_of_birth,
                gender=gender,
                photo=photo,
                is_admin=is_admin,
                registered_by=reg_by,
            )
            if is_admin:
                user.is_staff = True
                user.save()
            login(request, user)
            return redirect("profile_list")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


User = get_user_model()


def user_is_admin(user):
    updated_user = User.objects.get(pk=user.pk)
    return updated_user.is_superuser or updated_user.is_staff


@login_required
def profile_list(request):
    request.user.refresh_from_db()
    profiles = UserProfile.objects.all()
    return render(request, "core/profile_list.html", {"profiles": profiles})


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, "core/profile_detail.html", {"profile": profile})


@login_required
@user_passes_test(user_is_admin)
def profile_create(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            is_admin = form.cleaned_data.get("is_admin")
            if is_admin:
                user.is_staff = True
                user.save()
            reg_by = request.user.username
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data.get("full_name"),
                year_of_birth=form.cleaned_data.get("year_of_birth"),
                gender=form.cleaned_data.get("gender"),
                photo=form.cleaned_data.get("photo"),
                is_admin=is_admin,
                registered_by=reg_by,
            )
            return redirect("profile_list")
    else:
        form = RegistrationForm()
    return render(request, "core/profile_create.html", {"form": form})


@login_required
@user_passes_test(user_is_admin)
def profile_edit(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        year_of_birth = request.POST.get("year_of_birth")
        gender = request.POST.get("gender")
        is_admin = request.POST.get("is_admin") == "on"
        if "photo" in request.FILES:
            photo = request.FILES["photo"]
        else:
            photo = profile.photo

        profile.full_name = full_name
        profile.year_of_birth = year_of_birth
        profile.gender = gender
        profile.photo = photo
        profile.is_admin = is_admin
        profile.save()

        user = profile.user
        user.is_staff = is_admin
        user.save()

        return redirect("profile_detail", pk=profile.pk)
    return render(request, "core/profile_edit.html", {"profile": profile})


@login_required
@user_passes_test(user_is_admin)
def profile_delete(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        if profile.photo:
            profile.photo.delete(save=False)
        profile.user.delete()
        return redirect("profile_list")
    return render(request, "core/profile_confirm_delete.html", {"profile": profile})


@login_required
def registration_summary(request):
    sort = request.GET.get("sort", "-registration_date")
    allowed_sort = ["full_name", "registered_by", "registration_date"]
    field = sort.lstrip("-")
    if field not in allowed_sort:
        sort = "-registration_date"
    profiles = UserProfile.objects.all().order_by(sort)
    return render(
        request,
        "core/registration_summary.html",
        {"profiles": profiles, "current_sort": sort},
    )
