from rest_framework import viewsets, permissions, mixins, status, filters, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied 
from django_filters.rest_framework import DjangoFilterBackend


from posts.models import Post, Group, Comment, Follow, User
from .serializers import PostSerializer, GroupSerializer
from .serializers import CommentSerializer, FollowSerializer
from .permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """A ViewSet for Post API handling."""
    queryset = Post.objects.all()  # Скорее всего тест не limit/offset не проходит из за неправильной сортировки
    serializer_class = PostSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Create a model instance."""
        serializer.save(author=self.request.user)


    def perform_update(self, serializer):
        """Update a model instance."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        """Destroy a model instance."""
        if serializer.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """A ViewSet for Group API handling."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

# class FollowViesSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
#                     viewsets.GenericViewSet):
# class FollowViesSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
#                     viewsets.GenericViewSet, mixins.ListModelMixin):
# class FollowViesSet(generics.ListCreateAPIView):


class FollowViesSet(mixins.CreateModelMixin, viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    """A ViewSer for Follow API handling."""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.request.user.username)
    #     return user.follower



    

class CommentViewSet(viewsets.ModelViewSet):
    """A ViewSet for Comment API handling."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # def get_queryset(self):
    #     post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
    #     queryset = post.comments.select_related('author')
    #     return queryset

    # def perform_create(self, serializer):
    #     post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
    #     serializer.save(author=self.request.user, post=post)


    #***************************************************#
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




    #***************************************************#

    # def get_queryset(self): 
    #     """Make a custom queryset of a model instance.""" 
    #     post_id = self.kwargs.get('post_id') 
    #     new_queryset = Comment.objects.filter(post=post_id) 
    #     return new_queryset 
 
    # def perform_update(self, serializer): 
    #     """Uplate a model instance.""" 
    #     if serializer.instance.author != self.request.user: 
    #         raise PermissionDenied('Изменение чужого контента запрещено!') 
    #     super(CommentViewSet, self).perform_update(serializer) 
 
    # def perform_create(self, serializer): 
    #     """Create a model instance.""" 
    #     post_id = self.kwargs.get('post_id') 
    #     target_post = Post.objects.filter(pk=post_id) 
    #     serializer.save(author=self.request.user, post=target_post[0]) 
 
    # def perform_destroy(self, serializer): 
    #     """Destroy a model instance.""" 
    #     if serializer.author != self.request.user: 
    #         raise PermissionDenied('Удаление чужого контента запрещено!') 
    #     super(CommentViewSet, self).perform_destroy(serializer)

    #***************************************************#
    # def perform_destroy(self, serializer):  # Описываем процедуру удаления ()
    #     if serializer.author != self.request.user:
    #         return Response(serializer, status=status.HTTP_403_FORBIDDEN)
    #     super(CommentViewSet, self).perform_destroy(serializer)
