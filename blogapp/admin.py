from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


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
