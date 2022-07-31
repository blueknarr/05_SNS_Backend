from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.paginator import Paginator
from post.models import Post
from post.serializers import (
    PostCreateSerializer,
    PostPatchSerializer,
    PostDetailSerializer,
    PostListSerializer
)
from post.utils.utils import (
    get_user_id_from_token,
    get_post_detail,
    set_post_like_cnt,
    get_post_like_cnt,
    set_hash_tag,
    get_hash_tag
)


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''
        게시글 목록 가져오기 - 쿼리 스트링으로 4가지 옵션 선택
        1. 정렬 - default: -create_date (view, like)
        2. 검색 - 키워드로 filtering
        3. 해시태그 검색 - 키워드로 filtering
        4. pagination
        :param request: String
        :return: JSON
        '''
        try:
            # 1. 정렬 - like, view, create_date
            order_by = '-create_date'
            if request.GET.get('orderBy'):
                order_by = request.GET.get('orderBy')

            post = Post.objects.all().order_by(order_by)

            # 2. 검색 - 키워드를 입력받아 filtering
            if request.GET.get('search'):
                post = post.all().filter(title__contains=request.GET.get('search'))

            # 3. 해시 태그 검색 - 키워드를 입력받아 filtering
            filter_tags = False
            if request.GET.get('hashtags'):
                filter_tags = request.GET.get('hashtags')

            # 4. paginator
            page_cnt = 10
            if request.GET.get('paginator'):
                page_cnt = int(request.GET.get('paginator'))
            paginator = Paginator(post, page_cnt)

            page=1
            if request.GET.get('page'):
                page = int(request.GET.get('page'))
            post = paginator.get_page(page)

            list_serializer = PostListSerializer(post, many=True)

            res = []
            for row in list_serializer.data:
                tag = get_hash_tag(row['id'], filter_tags=filter_tags)
                if not tag:
                    continue

                like = get_post_like_cnt(row['id'])

                res.append({
                    '게시글 번호': row['id'],
                    '제목': row['title'],
                    '작성자': row['writer'],
                    '해시태그': tag,
                    '좋아요': like,
                    '조회수': row['view'],
                    '작성일': row['create_date'],
                })

            return Response({
                '게시글 목록': res
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({
                'message': f'게시글 목록을 가져올 수 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        '''
        게시글 등록
        :param request: String
        :return: JSON
        '''
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

                set_hash_tag(create_serializer.data['id'], request.data['tags'])
                return Response({
                    'message': '게시글을 등록했습니다.'
                }, status=status.HTTP_201_CREATED)
        return Response({
            'message': '게시글 등록을 실패했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        '''
        게시글 목록 가져오기
        :param post_id: Int
        :return: JSON
        '''
        post = get_post_detail(post_id)

        tag = get_hash_tag(PostDetailSerializer(post).data['id'])
        like = get_post_like_cnt(PostDetailSerializer(post).data['id'])

        res = {
            '게시글 번호': PostDetailSerializer(post).data['id'],
            '제목': PostDetailSerializer(post).data['title'],
            '작성자': PostDetailSerializer(post).data['writer'],
            '본문': PostDetailSerializer(post).data['content'],
            '해시태그': tag,
            '좋아요': like,
            '조회수': PostDetailSerializer(post).data['view'],
            '작성 날짜': PostDetailSerializer(post).data['create_date'],
            '수정 날짜': PostDetailSerializer(post).data['modify_date'],
            '삭제 유무': PostDetailSerializer(post).data['is_deleted']
        }

        if post:
            return Response({
                'message': f'{post_id}번 게시글을 불러왔습니다.',
                'post': res
            }, status=status.HTTP_200_OK)
        return Response({
            'message': f'{post_id}번 게시글이 없습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        '''
        게시글 수정
        :param request: String
        :param post_id: Int
        :return: JSON
        '''
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
        '''
        게시글 삭제
        :param request: String
        :param post_id: Int
        :return: JSON
        '''
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
        '''
        휴지통에 있는 게시글 목록
        :param request: String
        :return: JSON
        '''
        user_id = get_user_id_from_token(request.META['HTTP_AUTHORIZATION'].split()[1])

        if user_id == request.user.id:
            deleted_posts = Post.deleted_objects.filter(user_id=user_id).all()
            deleted_serializer = PostDetailSerializer(deleted_posts, many=True)

            res = []
            for row in deleted_serializer.data:
                tag = get_hash_tag(row['id'], row['is_deleted'])
                like = get_post_like_cnt(row['id'], row['is_deleted'])

                res.append({
                    '게시글 번호': row['id'],
                    '제목': row['title'],
                    '작성자': row['writer'],
                    '본문': row['content'],
                    '해시태그': tag,
                    '좋아요': like,
                    '조회수': row['view'],
                    '작성 날짜': row['create_date'],
                    '수정 날짜': row['modify_date'],
                    '삭제 유무': row['is_deleted']
                })
            return Response({
                'message': f'{request.user.user_name}의 휴지통에 있는 게시글 목록을 가져왔습니다.',
                'data': res
            }, status=status.HTTP_200_OK)
        return Response({
            'message': f'{request.user.user_name}의 휴지통에 있는 게시글 목록을 가져오지 못했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        '''
        휴지통에 있는 게시글 복원
        :param request: String
        :param post_id: Int
        :return: JSON
        '''
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


class PostLikeView(APIView):
    def post(self, request, post_id):
        '''
        좋아요, 좋아요 취소 기능을 하는 api
        좋아요 중복 불가
        :param request: String
        :param post_id: Int
        :return: JSON
        '''
        msg = set_post_like_cnt(request.data['sel'], request.user.id, post_id)

        return Response({
            'message': msg
        }, status=status.HTTP_200_OK)