from django_filters import filters
from django_filters import rest_framework as charfilter

from .models import Title


class TitleFilter(filters.FilterSet):
    name = charfilter(lookup_expr='icontains')
    category = charfilter(field_name='category__slug')
    genre = charfilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
