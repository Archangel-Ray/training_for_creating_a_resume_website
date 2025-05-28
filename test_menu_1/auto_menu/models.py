from django.db import models


class Menu(models.Model):
    menu_name = models.CharField(max_length=200, verbose_name="название меню")
    point_name = models.CharField(max_length=200, verbose_name="пункт меню")
    main_point = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Начальник"
    )
    slug = models.SlugField(null=False, db_index=True)

    def __str__(self):
        return self.point_name
