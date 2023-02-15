from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """A serializer for Post model."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """A serializer for Comment model."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """A serializer for Group model."""

    class Meta:
        fields = '__all__'
        model = Group

        # default=serializers.CurrentUserDefault())
    # user = serializers.StringRelatedField()
    # following = serializers.SlugRelatedField(many=True, queryset=User.objects.all())

class FollowSerializer(serializers.ModelSerializer):
    """A serializer for Follow model."""
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True, default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following',),
                message='Повтор'
            )
        ]

    def validate_following(self, following):
        if following == self.context['request'].user:
            raise serializers.ValidationError('Подписка на себя!')
        return following
