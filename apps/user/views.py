from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserCreateSerializer
from user.utils.utils import create_jwt_pair_for_user

User = get_user_model()


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
            user.delete()

            return Response({
                'message': '회원 탈퇴가 완료되었습니다.'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'message': '해당하는 유저가 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            return Response({
                'message': 'Login 성공',
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'email 또는 password를 확인해주세요.'
        })


class UserCreateView(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'message': '회원가입이 완료되었습니다.'
            }, status=status.HTTP_201_CREATED)