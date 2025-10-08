from django.contrib.auth.models import AbstractUser
from django.db import models


class CountryOfConsignment(models.Model):
    """
    Модель для списка стран с картинкой государственного флага.
    Страна будет выбираться пользователем в поле гражданство.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    state_flag = models.ImageField("Государственный флаг", upload_to="flag/", null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Название страны"
        verbose_name_plural = "Названия стран"

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Модель для списка городов. Город будет выбираться пользователем.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        ordering = ["name"]
        verbose_name = "Название города"
        verbose_name_plural = "Названия городов"

    def __str__(self):
        return self.name


class SupplementProfession(models.Model):
    """
    Специализации профессий.
    Модель недоработана. Необходимо сделать так чтоб пользователь мог выбрать несколько специализаций
    определённой профессии. Специализации должны отображаться соответственно выбранной профессии.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование")

    class Meta:
        ordering = ["name"]
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"

    def __str__(self):
        return self.name


class Profession(models.Model):
    """
    Модель для списка профессий. К профессии можно прикрепить несколько специализаций.
    Профессия будет выбираться пользователем.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    supplement_the_profession_of_the_user = models.ManyToManyField(
        SupplementProfession,
        related_name="supplement_profession"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"

    def __str__(self):
        return self.name


class Organization(models.Model):
    """
    Модель для списка организаций в которой работает пользователь.
    Организация имеет название и город месторасположения.
    ... Надо подумать, делать ли связь с полем "текущее место" работы в моём резюме.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")

    class Meta:
        ordering = ["name"]
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Модель для списка иностранных языков. Для определения знания языков пользователем.
    ... Надо подумать. Как сделать так чтоб был список без определения уровня.
    ... а уровень давался выбранному языку у каждого пользователя.
    """
    LANGUAGE_LEVEL = {
        "A1": "начальный",
        "A2": "элементарный",
        "B1": "средний",
        "B2": "выше среднего",
        "C1": "продвинутый",
        "C2": "профессиональный",
    }

    name = models.CharField(max_length=100, verbose_name="Язык")
    level = models.CharField(
        max_length=2,
        choices=LANGUAGE_LEVEL,
        verbose_name="уровень",
        default="A1"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Иностранный язык"
        verbose_name_plural = "Иностранные языки"

    def __str__(self):
        return f"{self.name}({self.level})"


class MyUser(AbstractUser):
    """
    Расширенная модель пользователя.
    Дополнена полями для хранения личной, профессиональной и контактной информации:
        - Личные данные:
            * photo — фотография пользователя.
            * biological_sex — пол (женский, мужской).
            * patronymic — отчество.
            * birthday — дата рождения.
            * citizenship — гражданство (связь с моделью CountryOfConsignment).
            * city — город проживания (связь с моделью City).
        - Профессиональная информация:
            * profession — основная профессия (связь с моделью Profession).
            * specialization_professions — дополнительные специализации (M2M с SupplementProfession).
            * the_level_of_professionalism — уровень профессионализма (от "ученик" до "супер-профессионал").
            * job — текущее место работы (связь с моделью Organization).
        - Языковые компетенции:
            * languages — знание иностранных языков (M2M с моделью Language).
        - Персональное описание:
            * motto — личный девиз.
            * about_me — свободное текстовое описание "Обо мне".

    Константы:
        PROFESSIONAL_LEVELS — справочник уровней профессионализма.
        BIOLOGICAL_SEX — справочник полов.
    """
    PROFESSIONAL_LEVELS = {
        "": "— Нет никакого —",
        "LR": "ученик",
        "BR": "начинающий",
        "LL": "небольшой опыт",
        "EX": "опыт есть",
        "PR": "профессионал",
        "SP": "супер-профессионал",
        "HB": "хобби",
    }

    BIOLOGICAL_SEX = {
        "": "— Не выбран —",
        "F": "женский",
        "M": "мужской"
    }

    photo = models.ImageField(
        "Собственное изображение",
        upload_to="user_s_photo/",
        null=True,
        blank=True,
    )
    biological_sex = models.CharField(
        max_length=1,
        choices=BIOLOGICAL_SEX,
        null=True,
        blank=True,
        verbose_name="Пол",
    )
    patronymic = models.CharField(max_length=100, verbose_name="Отчество", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="День рождения")
    citizenship = models.ForeignKey(
        CountryOfConsignment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Гражданство"
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")
    profession = models.ForeignKey(
        Profession, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Профессия"
    )
    specialization_professions = models.ManyToManyField(
        SupplementProfession,
        blank=True,
        related_name="supplement_user",
        verbose_name="Специализация",
    )
    the_level_of_professionalism = models.CharField(
        max_length=2,
        choices=PROFESSIONAL_LEVELS,
        null=True,
        blank=True,
        verbose_name="Уровень профессионализма",
    )
    job = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Текущее место работы",
    )
    languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name="knowledge_of_foreign_languages",
        verbose_name="Знание языков",
    )
    motto = models.CharField(max_length=1000, verbose_name="Мой девиз", null=True, blank=True)
    about_me = models.TextField(verbose_name="Обо мне", null=True, blank=True)

    def get_full_name_with_patronymic(self):
        """
        Возвращает полное имя с отчеством (если указано).
        Если ничего нет — fallback на username.
        """
        parts = [self.first_name, self.patronymic, self.last_name]
        full_name = " ".join([p for p in parts if p])  # собираем ФИО
        return full_name.strip() or self.username
