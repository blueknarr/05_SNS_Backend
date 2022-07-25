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