from django.contrib import admin

from .models import Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    # list_display = "__all__"
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ['under_menu']  # горизонтальное отображение окон таблиц многие ко многим на странице элементов
