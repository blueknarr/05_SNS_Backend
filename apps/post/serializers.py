from rest_framework import serializers
from post.models import Post


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
        fields = ['id', 'user', 'title', 'content']


class PostPatchSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.save()

        return instance

    class Meta:
        model = Post
        fields = ['title', 'content']


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'title', 'writer', 'content', 'like', 'view', 'hashtag', 'create_date', 'modify_date', 'is_deleted']


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'title', 'writer', 'create_date', 'like', 'view']