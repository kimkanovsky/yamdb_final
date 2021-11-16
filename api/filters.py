from django_filters.filters import CharFilter
from django_filters.rest_framework.filterset import FilterSet

from .models import Title


class TitleFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
