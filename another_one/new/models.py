from django.contrib.auth.models import AbstractUser
from django.db import models


class CountryOfConsignment(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    state_flag = models.ImageField("Государственный флаг", upload_to="flag/", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Название страны"
        verbose_name_plural = "Названия стран"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        ordering = ["name"]
        verbose_name = "Название города"
        verbose_name_plural = "Названия городов"

    def __str__(self):
        return self.name


class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        ordering = ["name"]
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")

    class Meta:
        ordering = ["name"]
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    PROFESSIONAL_LEVELS = {
        "LR": "ученик",
        "BR": "начинающий",
        "LL": "небольшой опыт",
        "EX": "опыт есть",
        "PR": "профессионал",
        "SP": "супер-профессионал",
        "HB": "хобби",
    }

    BIOLOGICAL_SEX = {
        "F": "женский",
        "M": "мужской"
    }

    photo = models.ImageField(
        "Собственное изображение",
        upload_to="user_s_photo/",
        null=True,
        blank=True,
    )
    biological_sex = models.CharField(
        max_length=1,
        choices=BIOLOGICAL_SEX,
        null=True,
        blank=True,
        verbose_name="Пол",
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="День рождения")
    citizenship = models.ForeignKey(
        CountryOfConsignment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Гражданство"
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")
    profession = models.ForeignKey(
        Profession, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Профессия"
    )
    the_level_of_professionalism = models.CharField(
        max_length=2,
        choices=PROFESSIONAL_LEVELS,
        null=True,
        blank=True,
        verbose_name="Уровень профессионализма",
    )
    job = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Текущее место работы",
    )
    motto = models.CharField(max_length=1000, verbose_name="Мой девиз", null=True, blank=True)
    about_me = models.TextField(verbose_name="Обо мне", null=True, blank=True)
