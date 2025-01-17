from api.serializers import (
    CommentsSerializer,
    GroupsSerializer,
    PostSerializer
)
from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы можете удалять только свои посты.")
        instance.delete()

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("Вы можете обновлять только свои посты.")
        serializer.save()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied(
                "Вы можете обновлять только свои комментарии.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                "Вы можете удалять только свои комментарии.")
        instance.delete()


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
