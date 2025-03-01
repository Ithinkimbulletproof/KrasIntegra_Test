from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]

    full_name = models.CharField("ФИО", max_length=255)
    year_of_birth = models.IntegerField("Год рождения")
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES)
    registration_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    photo = models.ImageField(
        "Фото пользователя", upload_to="photos/", blank=True, null=True
    )
    is_admin = models.BooleanField("Администратор", default=False)

    def __str__(self):
        return self.full_name
