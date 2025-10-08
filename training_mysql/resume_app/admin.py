from django.contrib import admin
from .models import (
    CountryOfConsignment,
    City,
    SupplementProfession,
    Profession,
    Organization,
    Language,
    MyUser
)

admin.site.register(CountryOfConsignment)
admin.site.register(City)
admin.site.register(SupplementProfession)
admin.site.register(Profession)
admin.site.register(Organization)
admin.site.register(Language)
admin.site.register(MyUser)
