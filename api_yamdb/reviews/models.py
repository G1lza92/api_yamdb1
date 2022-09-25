from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES,
        default='user',
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=32,
        blank=True,
        default=1111
    )
    password = None

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name[:30]


class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name[:30]


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.IntegerField(verbose_name='Год выпуска')
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
        ordering = ['id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:30]


class PubDateModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Review(PubDateModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'Оценка', choices=[(i, i) for i in range(1, 11)]
    )


class Comment(PubDateModel):
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
