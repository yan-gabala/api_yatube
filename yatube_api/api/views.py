from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Group
from .serializers import CommentSerializer, PostSerializer
from .serializers import GroupSerializer
from .permissions import IsOwnerOrReadOnly
from .permissions import AuthorOrReadOnlyPermission
               

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated,
                          AuthorOrReadOnlyPermission]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response(serializer.data,
                            status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, id=self.kwargs.get('post_id')) 
        serializer.save(author=self.request.user, post=post)
     
    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
