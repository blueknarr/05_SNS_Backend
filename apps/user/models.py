from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, user_name, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, user_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('이메일 주소'), unique=True)
    user_name = models.CharField('닉네임', max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    object = UserManager()

    def __str__(self):
        return f'id: {self.id}, email: {self.email}, user_name: {self.user_name}'

    class Meta:
        db_table = 'tb_users'
