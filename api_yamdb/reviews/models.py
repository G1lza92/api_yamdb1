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
    email = models.EmailField('Почта')
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

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.TextField()
    slug = models.SlugField()


class Genre(models.Model):
    name = models.TextField()
    slug = models.SlugField()


class Title(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL, related_name='titles'
    )


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
