# from django.urls import path, include
from .views import *
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import colored

router = DefaultRouter()
router.register('bloggers', BloggerViewSet, basename='bloggers')
router.register('all-blog', AllBlogVSet, basename='all-blog')

all_blogger_blogs = NestedDefaultRouter(
    router, 'bloggers', lookup='blogger')  # parent
all_blogger_blogs.register('blog', OwnBlogViewSet, basename='blog')  # child
# all_blogger_blogs.register('blogs', OwnerBlogListVSet, 'blogs')


comment_router = NestedDefaultRouter(all_blogger_blogs, 'blog', lookup='blog')
comment_router.register('comments', CommentVSet, basename='comments')

urlpatterns = router.urls \
    + all_blogger_blogs.urls \
    + comment_router.urls

for ptrn in urlpatterns:
    print(colored(ptrn, "blue"))
    print()
