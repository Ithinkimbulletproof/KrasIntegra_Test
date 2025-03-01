from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
import re


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.user:
            instance.user.is_staff = instance.is_admin
            if commit:
                instance.user.save()
        if commit:
            instance.save()
        return instance


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label="ФИО", required=True)
    year_of_birth = forms.IntegerField(label="Год рождения", required=True)
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES, label="Пол", required=True
    )
    photo = forms.ImageField(label="Фото пользователя", required=False)
    is_admin = forms.BooleanField(label="Сделать администратором", required=False)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if re.search(r"\d", full_name):
            raise forms.ValidationError("Имя не должно содержать цифры.")
        return full_name
