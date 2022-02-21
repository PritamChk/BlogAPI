
from rest_framework.serializers import ModelSerializer as ms

from .models import (
    Blog,  # TODO - YET TO SERIALIZE
    Blogger,
    Comment,  # TODO - YET TO DO SERIALIZE
)


class SimpleBloggerSerializer(ms):
    class Meta:
        model = Blogger
        fields = (
            "id",
            "username",
            # "first_name",
            # "last_name",
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


class BlogReadSerializer(ms):
    creator = SimpleBloggerSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'description', 'created_at',
                  'updated_at', 'creator')
        # read_only_field = ["creator"]


class BlogPostSerializer(ms):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'description')

    def create(self, validated_data):
        creator_id = self.context.get('creator_id')
        return Blog.objects.create(creator_id=creator_id, **validated_data)


class BlogPatchSerializer(ms):
    class Meta:
        model = Blog
        fields = ('title', 'description')
