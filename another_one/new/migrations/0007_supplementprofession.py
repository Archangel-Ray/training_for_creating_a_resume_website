# Generated by Django 5.2.2 on 2025-07-07 09:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0006_myuser_biological_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplementProfession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('supplement_the_profession_of_the_user', models.ManyToManyField(related_name='supplement', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Спецификация',
                'verbose_name_plural': 'Спецификации',
                'ordering': ['name'],
            },
        ),
    ]
