from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import username_validator


ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'
ROLES = [
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        'Почта',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LAST_NAME_MAX_LENGTH,
        blank=True
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=ROLE_USER,
        blank=True
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR


class CategoryGenreBase(models.Model):
    name = models.CharField(
        max_length=settings.NAME_MAX_LENGTH,
        db_index=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.SLUG_MAX_LENGTH,
        verbose_name='URL-метка',
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name[:30]


class Category(CategoryGenreBase):

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):

    class Meta(CategoryGenreBase.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


def get_current_year():
    return dt.now().year


class Title(models.Model):
    name = models.TextField(verbose_name='Название произведения')
    year = models.IntegerField(
        validators=[
            MaxValueValidator(
                limit_value=get_current_year,
                message='Произведение еще не вышло!'
            )
        ]
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:30]


class NoticeModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    text = models.TextField('Текст', help_text='Введите текст',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Выберите автора',
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = '%(class)ss'

    def __str__(self) -> str:
        return f'{self.pub_date} {self.author} {self.text:.30}'


class Review(NoticeModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        help_text='Выберите произведение',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Укажите оценку произведения (от 1 до 10)',
        validators=[
            MinValueValidator(
                1, message='Укажите оценку больше либо равную 1'
            ),
            MaxValueValidator(
                10, message='Укажите оценку меньше либо равную 10'
            ),
        ]
    )

    class Meta(NoticeModel.Meta):
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(NoticeModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Обзор',
        help_text='Выберите обзор',
    )

    class Meta(NoticeModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
