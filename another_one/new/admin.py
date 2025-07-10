from django.contrib import admin

from .models import (
    MyUser,
    CountryOfConsignment,
    City,
    Profession,
    SupplementProfession,
    Organization,
    Language,
)


class ProfessionAdmin(admin.ModelAdmin):
    filter_vertical = ["supplement_the_profession_of_the_user"]


admin.site.register(MyUser)
admin.site.register(CountryOfConsignment)
admin.site.register(City)
admin.site.register(SupplementProfession)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Organization)
admin.site.register(Language)
