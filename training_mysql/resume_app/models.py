from django.contrib.auth.models import AbstractUser
from django.db import models


class CountryOfConsignment(models.Model):
    """
    ������ ��� ������ ����� � ��������� ���������������� �����.
    ������ ����� ���������� ������������� � ���� �����������.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="��������")
    state_flag = models.ImageField("��������������� ����", upload_to="flag/", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "�������� ������"
        verbose_name_plural = "�������� �����"

    def __str__(self):
        return self.name


class City(models.Model):
    """
    ������ ��� ������ �������. ����� ����� ���������� �������������.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="��������")

    class Meta:
        ordering = ["name"]
        verbose_name = "�������� ������"
        verbose_name_plural = "�������� �������"

    def __str__(self):
        return self.name


class SupplementProfession(models.Model):
    """
    ������������� ���������.
    ������ ������������. ���������� ������� ��� ���� ������������ ��� ������� ��������� �������������
    ����������� ���������. ������������� ������ ������������ �������������� ��������� ���������.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="������������")

    class Meta:
        ordering = ["name"]
        verbose_name = "�������������"
        verbose_name_plural = "�������������"

    def __str__(self):
        return self.name


class Profession(models.Model):
    """
    ������ ��� ������ ���������. � ��������� ����� ���������� ��������� �������������.
    ��������� ����� ���������� �������������.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="��������")
    supplement_the_profession_of_the_user = models.ManyToManyField(
        SupplementProfession,
        related_name="supplement_profession"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "���������"
        verbose_name_plural = "���������"

    def __str__(self):
        return self.name


class Organization(models.Model):
    """
    ������ ��� ������ ����������� � ������� �������� ������������.
    ����������� ����� �������� � ����� �����������������.
    ... ���� ��������, ������ �� ����� � ����� "������� �����" ������ � ��� ������.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="��������")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="�����")

    class Meta:
        ordering = ["name"]
        verbose_name = "�����������"
        verbose_name_plural = "�����������"

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    ������ ��� ������ ����������� ������. ��� ����������� ������ ������ �������������.
    ... ���� ��������. ��� ������� ��� ���� ��� ������ ��� ����������� ������.
    ... � ������� ������� ���������� ����� � ������� ������������.
    """
    LANGUAGE_LEVEL = {
        "A1": "���������",
        "A2": "������������",
        "B1": "�������",
        "B2": "���� ��������",
        "C1": "�����������",
        "C2": "����������������",
    }

    name = models.CharField(max_length=100, verbose_name="����")
    level = models.CharField(
        max_length=2,
        choices=LANGUAGE_LEVEL,
        verbose_name="�������",
        default="A1"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "����������� ����"
        verbose_name_plural = "����������� �����"

    def __str__(self):
        return f"{self.name}({self.level})"


class MyUser(AbstractUser):
    """
    ����������� ������ ������������.
    ��������� ������ ��� �������� ������, ���������������� � ���������� ����������:
        - ������ ������:
            * photo � ���������� ������������.
            * biological_sex � ��� (�������, �������).
            * patronymic � ��������.
            * birthday � ���� ��������.
            * citizenship � ����������� (����� � ������� CountryOfConsignment).
            * city � ����� ���������� (����� � ������� City).
        - ���������������� ����������:
            * profession � �������� ��������� (����� � ������� Profession).
            * specialization_professions � �������������� ������������� (M2M � SupplementProfession).
            * the_level_of_professionalism � ������� ���������������� (�� "������" �� "�����-������������").
            * job � ������� ����� ������ (����� � ������� Organization).
        - �������� �����������:
            * languages � ������ ����������� ������ (M2M � ������� Language).
        - ������������ ��������:
            * motto � ������ �����.
            * about_me � ��������� ��������� �������� "��� ���".

    ���������:
        PROFESSIONAL_LEVELS � ���������� ������� ����������������.
        BIOLOGICAL_SEX � ���������� �����.
    """
    PROFESSIONAL_LEVELS = {
        "": "� ��� �������� �",
        "LR": "������",
        "BR": "����������",
        "LL": "��������� ����",
        "EX": "���� ����",
        "PR": "������������",
        "SP": "�����-������������",
        "HB": "�����",
    }

    BIOLOGICAL_SEX = {
        "": "� �� ������ �",
        "F": "�������",
        "M": "�������"
    }

    photo = models.ImageField(
        "����������� �����������",
        upload_to="user_s_photo/",
        null=True,
        blank=True,
    )
    biological_sex = models.CharField(
        max_length=1,
        choices=BIOLOGICAL_SEX,
        null=True,
        blank=True,
        verbose_name="���",
    )
    patronymic = models.CharField(max_length=100, verbose_name="��������", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="���� ��������")
    citizenship = models.ForeignKey(
        CountryOfConsignment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="�����������"
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="�����")
    profession = models.ForeignKey(
        Profession, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="���������"
    )
    specialization_professions = models.ManyToManyField(
        SupplementProfession,
        blank=True,
        related_name="supplement_user",
        verbose_name="�������������",
    )
    the_level_of_professionalism = models.CharField(
        max_length=2,
        choices=PROFESSIONAL_LEVELS,
        null=True,
        blank=True,
        verbose_name="������� ����������������",
    )
    job = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="������� ����� ������",
    )
    languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name="knowledge_of_foreign_languages",
        verbose_name="������ ������",
    )
    motto = models.CharField(max_length=1000, verbose_name="��� �����", null=True, blank=True)
    about_me = models.TextField(verbose_name="��� ���", null=True, blank=True)

    def get_full_name_with_patronymic(self):
        """
        ���������� ������ ��� � ��������� (���� �������).
        ���� ������ ��� � fallback �� username.
        """
        parts = [self.first_name, self.patronymic, self.last_name]
        full_name = " ".join([p for p in parts if p])  # �������� ���
        return full_name.strip() or self.username
