from django_filters import FilterSet
from .models import(
    Blogger,
)


class BloggerFilter(FilterSet):
    class Meta:
        model = Blogger
        fields = {
            'first_name':['istartswith','iexact','icontains',],    
            'last_name':['istartswith','iexact','icontains',],
            'email': ['istartswith','icontains','endswith'],
            "username": ["startswith","exact"],
            'last_login': ['exact', 'year__gt','year__lt'],
        }