from django_filters import FilterSet
from .models import(
    Blogger,
    Blog,
    Comment,
)


class BloggerFilter(FilterSet):
    class Meta:
        model = Blogger
        fields = {
            'first_name': ['istartswith'],
            'last_name': ['istartswith', 'icontains'],
            'email': ['icontains'],
            "username": ["startswith", "exact"],
            'last_login': ['year__gt', 'year__lt', "month__gt", "month__lt"],
        }


# class CommentFilter(FilterSet):
#     class Meta:
#         model = Comment
#         # TODO : filter fields to be added
#         # fields
