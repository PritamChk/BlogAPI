from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .filters import BloggerFilter


@admin.register(Blogger)
class BloggerAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'password1', 
                'password2', 
                'first_name', 
                'last_name', 
                "email"
            ),
        }),
    )

    search_fields = [
        "first_name__icontains",    
        "first_name__istartswith",    
    ]    
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        "last_login",
    )

    prepopulated_fields = {"username": ("last_name", "first_name")}
    raw_id_fields = ('groups', 'user_permissions')
