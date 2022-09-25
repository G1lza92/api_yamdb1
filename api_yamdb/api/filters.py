from django_filters import AllValuesFilter, CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):

    genre = AllValuesFilter(field_name='genre__slug')
    category = AllValuesFilter(field_name='category__slug')
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = [
            'genre',
            'category',
            'name',
            'year',
        ]
