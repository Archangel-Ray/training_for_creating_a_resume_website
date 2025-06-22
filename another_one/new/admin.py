from django.contrib import admin

from . import models

admin.site.register(models.MyUser)
admin.site.register(models.CountryOfConsignment)
admin.site.register(models.City)
admin.site.register(models.Profession)
admin.site.register(models.Organization)
