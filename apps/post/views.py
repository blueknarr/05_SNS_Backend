from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from post.models import Post
from post.serializers import (
    PostCreateSerializer,
    PostPatchSerializer,
    PostDetailSerializer,
    PostListSerializer
)
from post.utils.utils import (
    get_user_id_from_token,
    get_post_detail
)


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            post = Post.objects.all()
            list_serializer = PostListSerializer(post, many=True)

            res = []
            for row in list_serializer.data:
                res.append({
                    '제목': row['title'],
                    '작성자': row['writer'],
                    '해시태그': '',
                    '작성일': row['create_date'],
                    '좋아요': row['like'],
                    '조회수': row['view']
                })

            return Response({
                '게시글 목록': res
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'message': f'게시글 목록을 가져올 수 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

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


class PostDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        post = get_post_detail(post_id)

        if post:
            return Response({
                'message': f'{post_id}번 게시글을 불러왔습니다.',
                'post': PostDetailSerializer(post).data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': f'{post_id}번 게시글이 없습니다.'
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
            post = Post.objects.get(id=post_id)

            if user_id == request.user.id:
                post.delete()

                return Response({
                    'message': f'{post_id}번 게시글을 삭제했습니다.'
                }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'message': f'{post_id}번 게시글을 삭제할 수 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)


class PostRestoreView(APIView):
    def get(self, request):
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        if user_id == request.user.id:
            deleted_posts = Post.deleted_objects.filter(user_id=user_id).all()
            deleted_serializer = PostDetailSerializer(deleted_posts, many=True)

            res = []
            for row in deleted_serializer.data:
                res.append({
                    'id': row['id'],
                    'title': row['title'],
                    'writer': row['writer'],
                    'content': row['content'],
                    'like': row['like'],
                    'view': row['view'],
                    'create_date': row['create_date'],
                    'modify_date': row['modify_date'],
                    'is_deleted': row['is_deleted']
                })
            return Response({
                'message': f'{request.user.user_name}의 휴지통에 있는 게시글 목록을 가져왔습니다.',
                'data': res
            }, status=status.HTTP_200_OK)
        return Response({
            'message': f'{request.user.user_name}의 휴지통에 있는 게시글 목록을 가져오지 못했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        try:
            post = Post.deleted_objects.get(id=post_id)

            if user_id == request.user.id:
                post.restore()
                restore_serializer = PostDetailSerializer(post)

                return Response({
                    'message': f'{post_id}번 게시글을 복원했습니다.',
                    'data': restore_serializer.data
                }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'message': f'{post_id}번 게시글을 복원 할 수 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)