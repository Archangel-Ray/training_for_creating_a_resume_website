from django.contrib import admin
from django.db.models import (
    Case,
    When,
    F,
    Value,
    CharField
)

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
    Feedback,
)


class ProfessionAdmin(admin.ModelAdmin):
    filter_vertical = ["supplement_the_profession_of_the_user"]


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]
    ordering = ["-end_date"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("display_author", "content_short", "related_object", "created_at", "status")
    list_filter = ("status", "created_at", "content_type")
    search_fields = ("author_name", "author_user__username", "content")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            sort_author=Case(
                When(author_user__isnull=False, then=F("author_user__username")),
                When(author_user__isnull=True, then=F("author_name")),
                default=Value(""),
                output_field=CharField(),
            )
        )
        return qs.order_by("content_type", "object_id", "-created_at")

    def display_author(self, obj):
        if obj.author_user:
            return obj.author_user.get_full_name_with_patronymic()
        return obj.author_name or "пользователь не назвался"

    display_author.short_description = "Автор отклика"
    display_author.admin_order_field = "sort_author"

    def content_short(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content

    content_short.short_description = "Текст отклика"

    def related_object(self, obj):
        if obj.target:
            return f"{obj.content_type} → {obj.target}"
        return f"{obj.content_type} (id={obj.object_id})"

    related_object.short_description = "Объект"
    related_object.admin_order_field = "object_id"


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
