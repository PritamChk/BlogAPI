from django_filters import FilterSet
from .models import(
    Blogger,
    Blog,
    Comment,
)


class BloggerSearchFilter(FilterSet):
    class Meta:
        model = Blogger
        fields = {
            'first_name': ['istartswith'],
            'last_name': ['istartswith', 'icontains'],
            'email': ['icontains'],
            "username": ["startswith", "exact"],
            'last_login': ['year__gt', 'year__lt', "month__gt", "month__lt"],
        }


class BlogFilter(FilterSet):
    class Meta:
        model = Blog
        fields = {
            "title": ["icontains"],
            "description": ['icontains']
        }


# class CommentFilter(FilterSet):
#     class Meta:
#         model = Comment
#         # TODO : filter fields to be added
#         # fields
