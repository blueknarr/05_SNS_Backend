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


class PostPatchSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.save()

        return instance

    class Meta:
        model = Post
        fields = ['title', 'content']