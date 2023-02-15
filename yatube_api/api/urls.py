from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViesSet

router = routers.DefaultRouter()
router.register('v1/posts', PostViewSet, basename='poasts')
router.register('v1/groups', GroupViewSet, basename='groups')
router.register('v1/follow', FollowViesSet, basename='follow')
router.register(
    r'^v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path(r'v1/', include('djoser.urls.jwt')),
]
