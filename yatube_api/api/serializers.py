from rest_framework import serializers
from posts.models import Group, Post, Comment


class PostSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        source='author.username', read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'image', 'author', 'group',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'post']


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
