from rest_framework import viewsets, permissions, mixins, status, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, GroupSerializer
from .serializers import CommentSerializer, FollowSerializer
from .permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """A ViewSet for Post API handling."""
    queryset = Post.objects.all()  # Скорее всего тест не limit/offset не проходит из за неправильной сортировки
    serializer_class = PostSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    # print('-'*80)
    # print(queryset)
    # print('-'*80)
    # print(queryset[0])
    # print('-'*80)
    # print(type(queryset[0]))
    # print('-'*80)
    # print(dir(queryset[0]))
    # print('-'*80)
    # print(queryset[0].author)
    # print('-'*80)
    # print(type(queryset[0].author.get_username()))
    # print('-'*80)
    # print(queryset[0].author.get_username())
    # print('-'*80)

    def perform_create(self, serializer):
        """Create a model instance."""
        serializer.save(author=self.request.user)
    
    # def perform_destroy(self, serializer):  # Описываем процедуру удаления ()
    #     if serializer.author != self.request.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """A ViewSet for Group API handling."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class FollowViesSet(viewsets.ModelViewSet):  # Хотя возможно тут надо применить наследование от собственного (самописного !?) базового класса
    # """A ViewSer for Follow API handling."""
    # queryset = Follow.objects.all()
    # serializer_class = FollowSerializer
class FollowViesSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """A ViewSer for Follow API handling."""
    # pass
    permission_classes = (permissions.IsAuthenticated,)

    # queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    search_fields = ('following__username')

    # Не сработало
    # def get_queryset(self):
    #     return (Follow.objects.filter(user=self.request.user))
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return super().get_queryset()
    # Ошибки только прибавились.
    # def list(self, request):
    #     queryset = Follow.objects.all()
    #     serializer = FollowSerializer(queryset, many=True)
    #     return Response(serializer.data)



class CommentViewSet(viewsets.ModelViewSet):
    """A ViewSet for Comment API handling."""
    serializer_class = CommentSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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
    
    # def perform_update(self, serializer):
    #     if serializer.author == self.request.user:
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     super(CommentViewSet, self).perform_destroy(serializer)

    

    
    def perform_destroy(self, serializer):  # Описываем процедуру удаления ()
        print('*'*80)
        print(serializer)
        print('*'*80)
        print(dir(serializer))
        print('*'*80)
        if serializer.author != self.request.user:
            return Response(serializer, status=status.HTTP_403_FORBIDDEN)
        super(CommentViewSet, self).perform_destroy(serializer)
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        # super(CommentViewSet, self).perform_destroy(serializer)
