from django.contrib import admin

from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["point_name", "main_point", "menu_name"]
    list_filter = ["main_point"]
    ordering = ["main_point"]
    prepopulated_fields = {"slug": ("point_name",)}
