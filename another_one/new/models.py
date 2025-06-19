from django.contrib.auth.models import AbstractUser
from django.db import models


class CountryOfConsignment(models.Model):
    name = models.CharField(max_length=100)


class City(models.Model):
    name = models.CharField(max_length=100)


class Profession(models.Model):
    name = models.CharField(max_length=100)


class Organization(models.Model):
    name = models.CharField(max_length=100)
    city = models.OneToOneField(City, on_delete=models.SET_NULL, null=True, blank=True)


class MyUser(AbstractUser):
    pass
