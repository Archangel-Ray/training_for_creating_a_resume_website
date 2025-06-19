from django.contrib.auth.models import AbstractUser
from django.db import models


class CountryOfConsignment(models.Model):
    name = models.CharField(max_length=100)


class MyUser(AbstractUser):
    pass
