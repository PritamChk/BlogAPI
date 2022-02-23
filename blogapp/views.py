from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from termcolor import colored
from drf_psq import PsqMixin, psq, Rule
from .filters import BloggerFilter
from .models import Blog, Blogger, Comment
from .serializers import *
from .permissions import *


class BloggerViewSet(
    PsqMixin,
    ModelViewSet
):

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
        "email"]
    ordering_fields = [
        "first_name",
        "last_name",
        "email"
    ]
    permission_classes = [IsAdminUser]
    queryset = Blogger.objects.all()
    serializer_class = BloggerAdminSerializer
    psq_rules = {

        ("retrieve", 'partial_update', "update", 'destroy'): [
            Rule([IsAdminUser], BloggerAdminSerializer),
            Rule([IsAuthenticated & IsSelf], BloggerShow),
        ],
        "list": [
            Rule([IsAdminUser], BloggerAdminSerializer),
        ],

    }


class AllBloggerViewSet(PsqMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Blogger.objects.all()
    serializer_class = BloggerShow
    permission_classes = [IsAuthenticated]


class OwnerBlogListVSet(ListModelMixin, GenericViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    serializer_class = BlogReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.prefetch_related('comments')\
            .select_related('creator').filter(creator__id=self.kwargs['blogger_pk']).all()


class OwnerBlogCRUDSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    http_method_names = ["get", "put", "patch",
                         "post", "delete", "option", "head"]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    permission_classes = [IsAuthenticatedOrReadOnly, BlogEditPermission]

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [BlogEditPermission(),DjangoModelPermissions()]

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

    # def get_permissions(self):  # FIXME : NOT WORKING LIKE MOSH : lec : 11
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [BloggerEditPermission()]

    # def get_serializer_class(self):
    #     method = self.request.method
    #     if method == "PUT":
    #         return BloggerCreateSerializer
    #     elif method == "PATCH":
    #         return BloggerPatchSerializer
    #     return SimpleBloggerSerializer  # FIXME : NEED TO BE REMOVED

    # FIXME
    # @action(detail=False, methods=["GET", "PATCH"])
    # def me(self, request):
    #     blogger, created = Blogger.objects.get_or_create(
    #         id=self.request.user.id)
    #     if request.method == "GET":
    #         serializer = SimpleBloggerSerializer(blogger)
    #         return Response(serializer.data)
    #     elif request.method == "PUT":
    #         serializer = BloggerPatchSerializer(blogger, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)
