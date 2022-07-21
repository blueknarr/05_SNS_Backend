from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserCreateSerializer
from user.utils.utils import create_jwt_pair_for_user


class UserView(APIView):
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