from rest_framework import generics, viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from posts.models import Comment, Group, Post

from .serializers import CommentsSerializer, GroupsSerializer, PostSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("Вы можете удалять только свои посты.")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("Вы можете обновить только свои посты.")
        return super().update(request, *args, **kwargs)


class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)


class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied(
                "Вы можете удалять только свои комментарии.")
        return super().destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied(
                "Вы можете редактировать только свои комментарии.")

        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied(
                "Вы можете редактировать только свои комментарии.")

        return super().put(request, *args, **kwargs)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id, id=comment_id)


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(
            "POST", detail="Создание постов через API запрещено.")
