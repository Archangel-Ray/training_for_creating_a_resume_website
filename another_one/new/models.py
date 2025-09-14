from datetime import date
from typing import Optional, ClassVar

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
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


class Generalization(models.Model):
    """
    Абстрактная базовая модель, содержащая общее текстовое описание и наименование объекта.
    Используется как родитель для моделей, описывающих сущности резюме.
    (Навык, Рабочее место, Проект, Курс, Сертификат, Увлечения)
    """
    name = models.CharField(max_length=500, unique=True, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class StartAndEndDates(models.Model):
    """
    Абстрактная модель, добавляющая поля начала и окончания действия чего-либо
    (например, работы, проекта, курса), а также валидацию этих дат.
    """
    start_date = models.DateField(blank=True, null=True, verbose_name="Дата начала")
    end_date = models.DateField(blank=True, null=True, verbose_name="Дата окончания")

    start_date: Optional[date]
    end_date: Optional[date]

    def clean(self):
        # Проверка, если указана дата окончания, то обязательно должна быть дата начала
        if self.end_date is not None and self.start_date is None:
            raise ValidationError({
                'start_date': 'Дата начала обязательна, если указана дата окончания',
                'end_date': 'Не может быть указана без даты начала',
            })

        # Проверка, дата окончания не раньше даты начала
        if self.start_date:
            # Если даты окончания нет — проверка не нужна
            if self.end_date is None:
                return
            if self.start_date > self.end_date:
                raise ValidationError({
                    'end_date': 'Дата окончания не может быть раньше даты начала',
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def period_length_display(self):
        """Возвращает период от начала до завершения в удобочитаемом виде"""
        if not self.start_date:
            return "—"

        end = self.end_date or date.today()
        delta = relativedelta(end, self.start_date)

        parts = []

        if delta.years:
            parts.append(f"{delta.years} {self._declension(delta.years, 'год', 'года', 'лет')}")
            if delta.months:
                parts.append(f"{delta.months} {self._declension(delta.months, 'месяц', 'месяца', 'месяцев')}")
            if delta.days:
                parts.append(f"{delta.days} {self._declension(delta.days, 'день', 'дня', 'дней')}")

        elif delta.months:
            parts.append(f"{delta.months} {self._declension(delta.months, 'месяц', 'месяца', 'месяцев')}")
            if delta.days:
                parts.append(f"{delta.days} {self._declension(delta.days, 'день', 'дня', 'дней')}")

        else:
            parts.append(f"{delta.days} {self._declension(delta.days, 'день', 'дня', 'дней')}")

        return " ".join(parts)

    @staticmethod
    def _declension(number, form1, form2, form5):
        """Подбирает правильное склонение"""
        if number % 10 == 1 and number % 100 != 11:
            return form1
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return form2
        else:
            return form5

    class Meta:
        abstract = True


class LinkToTheOriginal(models.Model):
    """
    Абстрактная модель, содержащая ссылку на внешний источник — оригинал объекта
    (например, внешний проект, сертификат, сайт компании).
    """
    link_to_the_original = models.URLField(blank=True, null=True, verbose_name="Ссылка на оригинал")

    class Meta:
        abstract = True


class Skill(Generalization):
    """
    Навык с уровнем владения, которым владеет кандидат.
    Может быть связан с работами, курсами и проектами.
    """
    LEVEL_OF_OWNERSHIP = {
        "JN": "базовый",
        "MD": "средний",
        "SN": "продвинутый",
    }

    level = models.CharField(
        max_length=2,
        choices=LEVEL_OF_OWNERSHIP,
        null=True,
        blank=True,
        verbose_name="Уровень владения навыком",
    )
    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["Skill"]]

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class Working(Generalization, StartAndEndDates, LinkToTheOriginal):
    """
    Опыт работы кандидата.
    Содержит информацию о месте работы, периоде и используемых навыках.
    """
    position = models.CharField(max_length=255, verbose_name="Должность")
    used_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="i_worked_for",
        verbose_name="Навыки полученные на этой работе",
    )

    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["Working"]]

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"


class Project(Generalization, StartAndEndDates, LinkToTheOriginal):
    """
    Проект, выполненный кандидатом. Может быть связан с конкретным рабочим местом
    и содержит навыки, использованные в проекте.
    """
    used_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="projects",
        verbose_name="В проекте использованы навыки",
    )
    job = models.ForeignKey(
        Working,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="projects",
        verbose_name="Рабочее место проекта",
    )

    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["Project"]]

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class DeveloperOfTheCourse(Generalization, LinkToTheOriginal):
    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["DeveloperOfTheCourse"]]

    class Meta:
        verbose_name = "Автор курса"
        verbose_name_plural = "Авторы курсов"


class Course(Generalization, StartAndEndDates, LinkToTheOriginal):
    """
    Курс, пройденный кандидатом.
    Может содержать информацию о полученных навыках.
    """
    the_author_is_a_host = models.ForeignKey(
        DeveloperOfTheCourse,
        on_delete=models.SET_NULL,
        verbose_name="Автор или разработчик",
        null=True,
        blank=True
    )
    used_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="courses",
        verbose_name="Приобретённые навыки",
    )

    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["Course"]]

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Certificate(Generalization, LinkToTheOriginal):
    """
    Сертификат, подтверждающий завершение курса или достижение.
    Связан с курсом (один к одному), может содержать изображение и дату получения.
    """
    date = models.DateField(verbose_name="Дата получения")
    image = models.ImageField(
        "Изображение",
        upload_to="certificate/",
        null=True,
        blank=True,
    )
    course = models.OneToOneField(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="certificate",
        verbose_name="Где получен",
    )

    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["Certificate"]]

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class Passion(Generalization):
    """
    Личное увлечение или интерес кандидата.
    Не связано с профессиональной деятельностью, но помогает дополнить образ.
    """
    # объявляем менеджер явно, чтобы IDE его понимала
    objects: ClassVar[models.Manager["Passion"]]

    class Meta:
        verbose_name = "Увлечение"
        verbose_name_plural = "Увлечения"


class Feedback(models.Model):
    """
    Универсальная таблица для откликов под всеми компетенциями (навыки, проекты, курсы...)
    Как под списками, так и под конкретными компетенциями.
    """
    author_user = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    author_name = models.CharField(
        "Имя (для анонимов)",
        max_length=255,
        blank=True,
        null=True
    )
    content = models.TextField("Сообщение")

    # универсальная привязка к любому объекту
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Модель привязки")
    object_id = models.PositiveIntegerField(verbose_name="Идентификатор объекта")
    target = GenericForeignKey("content_type", "object_id")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Отредактировано")

    status = models.CharField(
        max_length=20,
        choices=[
            ("published", "Опубликовано"),
            ("pending", "На модерации"),
            ("hidden", "Скрыто"),
        ],
        default="published",
        verbose_name="Статус",
    )

    def display_author(self):
        """
        Универсальное отображение имени автора:
        - для зарегистрированных пользователей: ФИО или username
        - для анонимов: введённое имя или "пользователь не назвался".
        """
        if self.author_user:
            # кастомный метод из MyUser
            return self.author_user.get_full_name_with_patronymic()
        return self.author_name or "пользователь не назвался"

    display_author.short_description = "Автор отклика"

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отклик от {self.author_user or self.author_name or 'Аноним'} на {self.content_type} №{self.object_id}"
