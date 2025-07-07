from django.contrib import admin

from .models import (
    MyUser,
    CountryOfConsignment,
    City,
    Profession,
    SupplementProfession,
    Organization,
)

admin.site.register(MyUser)
admin.site.register(CountryOfConsignment)
admin.site.register(City)
admin.site.register(SupplementProfession)
admin.site.register(Profession)
admin.site.register(Organization)
