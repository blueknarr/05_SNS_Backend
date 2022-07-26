import jwt

from sns.settings import SIMPLE_JWT
from post.models import Post, PostLike, PostTag


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
        post_like, is_liked = PostLike.objects.get_or_create(post=post, user_id=user_id)

        if is_liked:
            msg = f'{post_id}번 게시글의 좋아요가 눌렸습니다.'
        else:
            msg = f'{post_id}번 게시글의 좋아요를 이미 눌렀습니다.'
    elif sel == 'dislike':
        post_like = PostLike.objects.filter(post=post).filter(user_id=user_id).first()
        post_like.delete()
        msg = f'{post_id}번 게시글의 좋아요를 취소했습니다.'

    return msg


def split_and_insert_hashtag(tags, id):
    tags = tags.split(',')
    print(id)
    post = Post.objects.get(id=id)

    for tag in tags:
        PostTag.objects.get_or_create(post=post, tag=tag)

