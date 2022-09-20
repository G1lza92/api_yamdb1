from django.db import models


class Categories(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:30]


class Genres(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.title[:30]


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    pub_date = models.DateTimeField(verbose_name='Дата выхода')
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        verbose_name='Жанр',
        related_name='titles'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.title[:30]
