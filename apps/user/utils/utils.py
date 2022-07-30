from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

def create_jwt_pair_for_user(user: User):
    '''
    access token, refresh token 발급
    :param user: String
    :return: JSON
    '''
    refresh = RefreshToken.for_user(user)
    token = {
        'access_token': str(refresh.access_token),
        'refresh_toekn': str(refresh)
    }
    return token