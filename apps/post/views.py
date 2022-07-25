from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from post.models import Post
from post.serializers import PostCreateSerializer, PostPatchSerializer
from post.utils.utils import get_user_id_from_token
from user.models import User


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        if user_id == request.user.id:
            create_serializer = PostCreateSerializer(
                data={
                    'user': user_id,
                    'title': request.data['title'],
                    'content': request.data['content']
                })

            if create_serializer.is_valid(raise_exception=True):
                create_serializer.save()

                return Response({
                    'message': '게시글을 등록했습니다.'
                }, status=status.HTTP_201_CREATED)
        return Response({
            'message': '게시글 등록을 실패했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        if user_id == request.user.id:
            post = get_object_or_404(Post, id=post_id)
            patch_serializer = PostPatchSerializer(data=request.data, instance=post)

            if patch_serializer.is_valid(raise_exception=True):
                patch_serializer.save()

                return Response({
                    'message': '게시글을 수정했습니다.'
                }, status=status.HTTP_200_OK)
        return Response({
            'message': '게시글 수정을 실패했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        try:
            post = Post.objects.get(id=request.data['post_id'])
            if user_id == request.user.id:
                post.delete()
                return Response({
                    'message': f'{request.data["post_id"]}번 게시글을 삭제했습니다.'
                }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'message': f'{request.data["post_id"]}번 게시글을 삭제할 수 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)