import jwt

from sns.settings import SIMPLE_JWT
from post.models import Post, PostTag


def get_user_id_from_token(token):
    '''
    access_token을 decode하여 user_id를 비교하여 본인 여부 확인
    :param token: String
    :return: String
    '''
    decode = jwt.decode(
        token,
        SIMPLE_JWT['SIGNING_KEY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']],
    )
    return decode['user_id']


def get_post_detail(post_id):
    '''
    게시글을 열람했을 때 조회수 증가
    :param post_id: Int
    :return: Boolean
    '''
    post = Post.objects.filter(id=post_id).first()

    if post:
        post.view += 1
        post.save()
        return post
    return False


def set_post_like_cnt(sel, user_id, post_id):
    '''
    게시글에 대한 좋아요 기능
    하나의 게시글에 좋아요를 중복 선택 불가
    :param sel: String
    :param user_id: Int
    :param post_id: Int
    :return: String
    '''
    post = Post.objects.get(id=post_id)

    if sel == 'like':
        is_liked = post.like.filter(id=user_id).first()

        if is_liked:
            msg = f'{post_id}번 게시글의 좋아요를 이미 눌렀습니다.'
        else:
            post.like.add(user_id)
            msg = f'{post_id}번 게시글의 좋아요를 눌렸습니다.'
    elif sel == 'dislike':
        post.like.remove(user_id)
        msg = f'{post_id}번 게시글의 좋아요를 취소했습니다.'

    return msg


def get_post_like_cnt(post_id, is_deleted=False):
    '''
    게시글의 좋아요 개수
    :param post_id: Int
    :param is_deleted: Boolean
    :return: Int
    '''
    if is_deleted:
        post = Post.deleted_objects.get(id=post_id)
    else:
        post = Post.objects.get(id=post_id)
    cnt = post.like.all()

    return cnt.count()


def set_hash_tag(post_id, tags):
    '''
    게시글에 대한 해시 태크 생성
    :param post_id: Int
    :param tags: List
    '''
    post = Post.objects.get(id=post_id)

    for name in tags.split(','):
        tag, is_created = PostTag.objects.get_or_create(tag=name)
        post.hashtag.add(tag)


def get_hash_tag(post_id, is_deleted=False, filter_tags=None):
    '''
    게시글 해시테그
    :param post_id: Int
    :param is_deleted: Boolean
    :param filter_tags: List
    :return: List
    '''
    if is_deleted:
        post = Post.deleted_objects.get(id=post_id)
    else:
        post = Post.objects.get(id=post_id)

    tags = post.hashtag.all()
    if filter_tags:
        filtered = dict.fromkeys(filter_tags.split(','), True)

        cnt = 0
        for row in tags:
            if row.tag[1:] in filtered:
                cnt+=1
        if cnt != len(filtered):
            return False

    res = [row.tag for row in tags]
    return res
