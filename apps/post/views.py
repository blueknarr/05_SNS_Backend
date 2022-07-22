from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from post.models import Post
from post.serializers import PostCreateSerializer
from post.utils.utils import get_user_id_from_token
from user.models import User


class PostCreateView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        if user_id == request.user.id:
            user = User.objects.filter(id=user_id).first()
            Post.objects.create(
                user=user,
                writer=user.user_name,
                **request.data
            )

            return Response({
                'message': '게시글 등록을 성공했습니다.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': '게시글 등록을 실패했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
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