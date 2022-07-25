from rest_framework import serializers
from post.models import Post
from user.models import User


class PostCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        post = Post.objects.create(
            user=validated_data.get('user'),
            writer=validated_data.get('user').user_name,
            title=validated_data['title'],
            content=validated_data['content']
        )
        return post

    class Meta:
        model = Post
        fields = ['user', 'title', 'content']
