from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserCreateSerializer


class UserCreateView(APIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({
                'message': '회원가입이 완료되었습니다.'
            }, status=status.HTTP_201_CREATED)