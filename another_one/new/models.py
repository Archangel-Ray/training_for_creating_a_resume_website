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
    pass
