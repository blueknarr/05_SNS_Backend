from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    user_name = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(write_only=True)

    def validated_email(self, email):
        get_user = User.object.filter(email__iexact=email)

        if get_user.count() > 0:
            raise serializers.ValidationError(
                _('이미 등록한 이메일 주소 입니다.')
            )
        return email

    def validate_user_name(self, user_name):
        get_user = User.object.filter(user_name__iexact=user_name)

        if get_user.count() > 0:
            raise serializers.ValidationError(
                _('이미 등록한 유저 이름입니다.')
            )
        return user_name

    def validate(self, data):
        data['email'] = self.validated_email(data['email'])
        data['user_name'] = self.validate_user_name(data['user_name'])
        return data

    def create(self, valid_data):
        user = User.object.create_user(
            email=valid_data['email'],
            user_name=valid_data['user_name'],
            password=valid_data['password']
        )
        return user
