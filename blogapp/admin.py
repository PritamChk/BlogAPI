from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import *


@admin.register(Blogger)
class BloggerAdmin(UserAdmin):
    # fieldsets = UserAdmin.fieldsets + (
    #     (_('FOLLOWER-FOLLOWING'), 
    #     {
    #          'fields': ('follows', 'followed_by')
    #     }
    #     ),
    # )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'password1', 
                'password2', 
                'first_name', 
                'last_name', 
                "email",
                # "follows",
                # "followed_by"
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
        # "followed_by",
    )

    prepopulated_fields = {"username": ("last_name", "first_name")}
    raw_id_fields = ('groups', 'user_permissions')
