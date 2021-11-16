from django_filters import CharFilter
from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.filterset.FilterSet):
    name = CharFilter(lookup_expr='icontains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
