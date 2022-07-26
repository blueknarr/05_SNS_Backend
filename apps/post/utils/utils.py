import jwt

from sns.settings import SIMPLE_JWT
from post.models import Post


def get_user_id_from_token(token):
    decode = jwt.decode(
        token,
        SIMPLE_JWT['SIGNING_KEY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']],
    )
    return decode['user_id']


def get_post_detail(post_id):
    post = Post.objects.filter(id=post_id).first()

    if post:
        post.view += 1
        post.save()
        return post
    return False


def set_post_like_cnt(sel, user_id, post_id):
    post = Post.objects.get(id=post_id)

    if sel == 'like':
        is_liked = post.like.filter(id=user_id).first()

        if is_liked:
            msg = f'{post_id}번 게시글의 좋아요를 이미 눌렀습니다.'
        else:
            msg = f'{post_id}번 게시글의 좋아요가 눌렸습니다.'
    elif sel == 'dislike':
        post.like.remove(user_id)
        msg = f'{post_id}번 게시글의 좋아요를 취소했습니다.'

    return msg