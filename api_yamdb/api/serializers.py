from django.core.exceptions import ValidationError
<<<<<<< HEAD
from django.core.validators import RegexValidator
=======
>>>>>>> 2f0c143 (validation)
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import UsernameValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class TitleDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = fields


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if (
            self.context['request'].method != 'POST'
            or not get_object_or_404(
                Title, pk=self.context['view'].kwargs.get('title_id')
            ).reviews.filter(author=self.context['request'].user).exists()
        ):
            return data
        raise ValidationError(
            'Нельзя добавить второй отзыв на то же самое произведение.'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
<<<<<<< HEAD
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя содержит недоступные символы'
            )
        ]
    )
    email = serializers.EmailField()

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Для имени пользователя нельзя использовать "me"'
            )
        return value
=======
        validators=[UsernameValidator()]
    )
    email = serializers.EmailField()
>>>>>>> 2f0c143 (validation)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
<<<<<<< HEAD
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя содержит недоступные символы'
            )
        ]
=======
        validators=[UsernameValidator()]
>>>>>>> 2f0c143 (validation)
    )
    confirmation_code = serializers.CharField()
