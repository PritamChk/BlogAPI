
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import ModelSerializer as ms
from rest_framework.serializers import SerializerMethodField as smf, StringRelatedField

from .models import Blog, Blogger, Comment


class BloggerAdminSerializer(ms):
    class Meta:
        model = Blogger
        fields = '__all__'


class BloggerShow(ms):
    username = StringRelatedField(read_only=True)

    class Meta:
        model = Blogger
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class BloggerReadOnlySerializer(ms):
    username = StringRelatedField(read_only=True)

    class Meta:
        model = Blogger
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        read_only_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


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

# ----------------------Blog Serializers -----------------------------------


class BlogReadSerializer(ms):
    creator = SimpleBloggerSerializer(read_only=True)
    no_of_comments = smf(method_name='count_commentor', read_only=True)

    def count_commentor(self, obj: Blog):
        return obj.comments.count()

    class Meta:
        model = Blog
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'creator',
            "no_of_comments",
        )


class BlogPostSerializer(ms):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'description')  # FIXME : id removed

    def create(self, validated_data):
        creator_id = self.context.get('creator_id')
        return Blog.objects.create(creator_id=creator_id, **validated_data)


class BlogPatchSerializer(ms):
    class Meta:
        model = Blog
        fields = ('title', 'description')

# ----------------COMMENT SERIALIZERS ---------------------------------------


class CommentsGetSerializer(ms):
    class Meta:
        model = Comment
        fields = (
            "id",
            'comment_body',
            'created_at',
            'updated_at',
        )


class CommentsPostSerializer(ms):
    class Meta:
        model = Comment
        fields = (
            "id",
            'comment_body',
        )

    def create(self, validated_data):
        blog_id = self.context.get('blog_pk')
        commentor_id = self.context.get('blogger_pk')
        return Comment.objects.create(
            commentor_id=commentor_id,
            blog_id=blog_id,
            **validated_data
        )


class CommentsPatchSerializer(ms):
    class Meta:
        model = Comment
        fields = (
            'comment_body',
        )


class BloggerSignUpSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        # model = Blogger
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class CurrentBloggerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )
