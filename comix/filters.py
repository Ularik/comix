import django_filters
from .models import Comix


class ComixFilter(django_filters.FilterSet):
    class Meta:
        model = Comix
        fields = {
            'watches': ['lt', 'gt'],
            'common_grade': ['lt', 'gt'],
        }