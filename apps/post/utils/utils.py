import jwt

from sns.settings import SIMPLE_JWT


def get_user_id_from_token(token):
    decode = jwt.decode(
        token,
        SIMPLE_JWT['SIGNING_KEY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']],
    )
    return decode['user_id']