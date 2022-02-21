from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Blogger, Blog, Comment
from .serializers import *
from .filters import BloggerFilter


class BloggerViewSet(ModelViewSet):
    http_method_names = [
        # "get", #FIXME : NEED TO BE REMOVED
        "post",
        "patch",
        "delete",
        "head",
        "option"
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = BloggerFilter
    search_fields = ["first_name", "last_name", "username", "email"]
    ordering_fields = ["first_name", "last_name", "email"]
    queryset = Blogger.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerCreateSerializer
        elif method == "PATCH":
            return BloggerPatchSerializer
        return SimpleBloggerSerializer  # FIXME : NEED TO BE REMOVED


class BlogVSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "option", "head"]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        return Blog.objects.select_related('creator')\
            .prefetch_related('comments')\
            .filter(creator__id=self.kwargs.get('blogger_pk'))

    def get_serializer_class(self):
        method = self.request.method
        if method == "PATCH":
            return BlogPatchSerializer
        elif method == "POST":
            return BlogPostSerializer
        return BlogReadSerializer

    def get_serializer_context(self):
        return {"creator_id": self.kwargs['blogger_pk']}


class AllBlogVSet(ListModelMixin, GenericViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    queryset = Blog.objects.select_related(
        'creator').prefetch_related('comments').all()
    serializer_class = BlogReadSerializer


class CommentVSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "option", "head"]

    def get_queryset(self):
        return Comment.objects.select_related('blog')\
            .select_related('commentor')\
            .filter(
                commentor__id=self.kwargs.get('blogger_pk'),
                blog__id=self.kwargs.get('blogs_pk')
        )

    def get_serializer_context(self):
        return {
            'blogger_pk': self.kwargs['blogger_pk'],
            'blog_pk': self.kwargs['blogs_pk']
        }

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return CommentsPostSerializer
        elif method == "PATCH":
            return CommentsPatchSerializer
        return CommentsGetSerializer
