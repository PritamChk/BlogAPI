
from rest_framework.serializers import ModelSerializer as ms

from .models import (
    Blog, #TODO - YET TO SERIALIZE
    Blogger,  
    Comment, #TODO - YET TO DO SERIALIZE
)


class SimpleBloggerSerializer(ms):
    class Meta:
        model = Blogger
        fields = (
            "id",
            "username",
            "get_full_name",
        )


class BloggerCreateSerializer(ms):
    class Meta:
        model = Blogger
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )

class BloggerPatchSerializer(ms):
    class Meta:
        model = Blogger
        fields = (
            "first_name",
            "last_name",
            "email",
        )

