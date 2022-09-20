from rest_framework import serializers
from reviews.models import Categories, Genres, Title


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genres.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'
