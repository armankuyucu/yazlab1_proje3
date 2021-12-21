from django.contrib.auth.models import User
import django_filters
from .models import Document
from django_filters import CharFilter


class Query2Filter(django_filters.FilterSet):
    term = CharFilter(field_name='term', lookup_expr='icontains')
    lecture_name = CharFilter(field_name='lecture_name', lookup_expr='icontains')

    class Meta:
        model = Document
        fields = ('user', 'term', 'lecture_name')


class Query1Filter(django_filters.FilterSet):
    author = CharFilter(field_name='author', lookup_expr='icontains')
    lecture_name = CharFilter(field_name='lecture_name', lookup_expr='icontains')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    keywords = CharFilter(field_name='keywords', lookup_expr='icontains')
    term = CharFilter(field_name='term', lookup_expr='icontains')

    class Meta:
        model = Document
        fields = ('author', 'lecture_name', 'title', 'keywords', 'term')
