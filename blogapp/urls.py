# from django.urls import path, include
from .views import *
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import colored

router = DefaultRouter()
# router.register('blogger',BloggerListVSet,'blogger')
router.register('blogger', BloggerViewSet, basename='blogger')
router.register('all-blog', AllBlogVSet, basename='all-blog')  # TODO

blogger_router = NestedDefaultRouter(router, 'blogger', lookup='blogger')
blogger_router.register('blogs', BlogVSet, basename='blogger-blogs')

urlpatterns = router.urls \
    + blogger_router.urls

for ptrn in urlpatterns:
    print(colored(ptrn, "blue"))
    print()
