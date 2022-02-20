from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.views import FilterView
from .models import Blogger, Blog, Comment
from .serializer import *
# from .filters import BloggerSearchFilter, BlogFilter


class BloggerViewSet(ModelViewSet, FilterView):
    http_method_names = [
        "get", "post",
        "patch",
        "delete", "head", "option"]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filter_class = BlogFilter
    filterset_fields = ["first_name"]
    search_fields = ["first_name"]
    ordering_fields = ["first_name", "last_name"]
    queryset = Blogger.objects.all()

    # def get_queryset(self):
    # return Blogger.objects.filter(id=self.kwargs.get('pk'))

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerCreateSerializer
        elif method == "PATCH":
            return BloggerPatchSerializer
        return SimpleBloggerSerializer

    def get_serializer_context(self):
        return {"request": self.request}
