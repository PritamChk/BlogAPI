
from django_filters.rest_framework import DjangoFilterBackend
from drf_psq import PsqMixin, Rule, psq
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import (AND, NOT, OR, AllowAny,
                                        DjangoModelPermissions, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from termcolor import colored

from .filters import BloggerFilter
from .models import Blog, Blogger, Comment
from .permissions import *
from .serializers import *


class BloggerViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "delete", "head", "options"]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filter_class = BloggerFilter
    search_fields = [
        "first_name",
        "last_name",
        "username",
        "email"
    ]
    ordering_fields = [
        "first_name",
        "last_name",
        "email"
    ]
    permission_classes = [IsAdminUser | (IsAuthenticated & IsSelf)]
    queryset = Blogger.objects.all()
    serializer_class = BloggerAdminSerializer

    def get_permissions(self):
        method = self.request.method
        if method == "GET":
            return [IsAuthenticated()]
        elif method in ["PATCH", "DELETE"]:
            # return [IsAuthenticated(), IsSelf()] #FIXME : Admin should not patch
            return [AND(IsAuthenticated(), IsSelf())]
        return [IsAdminUser()]

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerAdminSerializer
        elif method == "PATCH":
            return BloggerPatchSerializer
        return BloggerShow


class OwnBlogViewSet(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    serializer_class = BlogReadSerializer
    permission_classes = [IsAdminUser | (IsAuthenticated & IsBlogOwner)]
    # queryset = Blog.objects.prefetch_related(
    #     'comments').select_related('creator').all()

    def get_queryset(self):
        blog_qset = Blog.objects.prefetch_related(
            'comments').select_related('creator')
        return blog_qset.filter(creator__id=self.kwargs.get('blogger_pk'))

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PATCH":
            return BlogPatchSerializer
        elif self.request.method == "POST":
            return BlogPostSerializer
        return BlogReadSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return[IsAuthenticated()]
        elif self.request.method in ["POST", "PATCH", "DELETE"]:
            return [AND(IsAuthenticated(), IsBlogOwner())]
        return [IsAdminUser()]

    def get_serializer_context(self):
        return {"creator_id": self.request.user.id}


class AllBlogVSet(ListModelMixin, GenericViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    queryset = Blog.objects.select_related(
        'creator').prefetch_related('comments').all()
    serializer_class = BlogReadSerializer


class CommentVSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "option", "head"]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [OR(IsAdminUser(), IsAuthenticated())]
        elif self.request.method in ["PATCH", "POST","DELETE"]:
            return [AND(IsAuthenticated(), IsOwnerOfComment())]
        return [
            OR(
                IsAdminUser(),
                AND(
                    IsAuthenticated(),
                    IsOwnerOfComment()
                )
            )
        ]

    def get_queryset(self):
        return Comment.objects.select_related('blog')\
            .select_related('commentor')\
            .filter(
                # commentor__id=self.kwargs.get('blogger_pk'),
                blog__id=self.kwargs.get('blog_pk')
        )

    def get_serializer_context(self):
        return {
            'blogger_pk': self.request.user.id,
            'blog_pk': self.kwargs['blog_pk']
        }

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return CommentsPostSerializer
        elif method == "PATCH":
            return CommentsPatchSerializer
        return CommentGetSerializer
