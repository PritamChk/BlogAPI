# from django.urls import path, include
from .views import *
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import colored

router = DefaultRouter()
router.register('blogger', BloggerViewSet, basename='blogger')
router.register('all-blog', AllBlogVSet, basename='all-blog')

blog_router = NestedDefaultRouter(
    router, 'blogger', lookup='blogger')  # parent
blog_router.register('blog', OwnerBlogCRUDSet, basename='blog')  # child
blog_router.register('blogs',OwnerBlogListVSet,'blogs')

comment_router = NestedDefaultRouter(blog_router, 'blog', lookup='blog')
comment_router.register('comments', CommentVSet, basename='comments')

urlpatterns = router.urls \
    + blog_router.urls \
    + comment_router.urls

for ptrn in urlpatterns:
    print(colored(ptrn, "blue"))
    print()