from django.db import models
from django.utils.text import slugify


class Menu(models.Model):
    name = models.CharField(max_length=200, verbose_name="пункт меню")
    under_menu = models.ManyToManyField(
        'self',
        related_name="+",
        null=True,
        blank=True,
        verbose_name="под уровень"
    )
    slug = models.SlugField(null=False, db_index=True, allow_unicode=True)

    def __str__(self):
        return self.name
