from django.contrib import admin

from .models import (
    MyUser,
    CountryOfConsignment,
    City,
    Profession,
    SupplementProfession,
    Organization,
    Language,
    Skill,
    Working,
    Project,
    Course,
    Certificate,
    Passion,
    DeveloperOfTheCourse,
)


class ProfessionAdmin(admin.ModelAdmin):
    filter_vertical = ["supplement_the_profession_of_the_user"]


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]


admin.site.register(MyUser)
admin.site.register(CountryOfConsignment)
admin.site.register(City)
admin.site.register(SupplementProfession)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Organization)
admin.site.register(Language)
admin.site.register(Skill)
admin.site.register(Working)
admin.site.register(Project)
admin.site.register(Course, CourseAdmin)
admin.site.register(Certificate)
admin.site.register(Passion)
admin.site.register(DeveloperOfTheCourse)
