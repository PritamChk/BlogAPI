# from django.urls import path, include
from os import sep
from .views import *
from rest_framework_nested.routers import DefaultRouter
from termcolor import colored

router = DefaultRouter()
# router.register('blogger',BloggerListVSet,'blogger')
router.register('blogger', BloggerViewSet, basename='blogger')

for ptrn in router.urls:
    print(colored(ptrn, "yellow"))
    print()
    
urlpatterns = router.urls
