from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, GroupSerializer
from .serializers import CommentSerializer, FollowSerializer
from .permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """A ViewSet for Post API handling."""
    queryset = Post.objects.all()  # Скорее всего тест не limit/offset не проходит из за неправильной сортировки
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly)
    # permission_classes = (AuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination


    def perform_create(self, serializer):
        """Create a model instance."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """A ViewSet for Group API handling."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViesSet(viewsets.ModelViewSet):  # Хотя возможно тут надо применить наследование от собственного (самописного !?) базового класса
    """A ViewSer for Follow API handling."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """A ViewSet for Comment API handling."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Make a custom queryset of a model instance."""
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        """Create a model instance."""
        post_id = self.kwargs.get('post_id')
        target_post = Post.objects.filter(pk=post_id)
        serializer.save(author=self.request.user, post=target_post[0])
