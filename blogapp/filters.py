#FIXME: Whole Filtering 
# from django_filters import FilterSet
# # from django_filters import Sea
# from .models import(
#     Blogger,
#     Blog,
#     Comment,
# )


# class BloggerSearchFilter(FilterSet):
#     class Meta:
#         model = Blogger
#         fields = {
#             'first_name': ['istartswith', 'iexact' ],
#             'last_name': ['istartswith', 'iexact', 'icontains', ],
#             'email': ['istartswith', 'icontains', 'endswith'],
#             "username": ["startswith", "exact"],
#             'last_login': ['exact', 'gt', 'lt'],
#             # "blogs":[]
#         }


# class BlogFilter(FilterSet):
#     class Meta:
#         model = Blog
#         # TODO : filter fields to be added
#         fields = {
#             "title":["icontains"],
#             "creator":[""]    
#         }
    


# # class CommentFilter(FilterSet):
# #     class Meta:
# #         model = Comment
# #         # TODO : filter fields to be added
# #         # fields
