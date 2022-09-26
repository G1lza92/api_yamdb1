from django.conf import settings
from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    list_editable = ('role', )
    search_fields = ('username', 'email', )
    list_filter = ('role', )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('name', 'slug', )
    search_fields = ('name', 'slug', )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('category', )
    search_fields = ('name', 'description', )
    list_filter = ('category', 'genre', )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'pub_date',
        'text',
        'author',
        'title',
        'score',
    )
    list_editable = ('author', 'title', 'score', )
    search_fields = ('text', )
    list_filter = ('author', 'title', 'score', )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'pub_date',
        'text',
        'author',
        'review',
    )
    list_editable = ('author', 'review', )
    search_fields = ('text', )
    list_filter = ('author', 'review', )
    empty_value_display = settings.ADMIN_MODEL_EMPTY_VALUE
