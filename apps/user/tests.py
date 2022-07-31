from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class UserAccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
        db = get_user_model()

        cls.super_user = db.objects.create_superuser(
            'testadmin@gmail.com', 'testsuper', 'password'
        )
        cls.user = db.objects.create_user(
            'user@gmail.com', 'testuser', 'password'
        )
        cls.login_context = {
            'email': 'user@gmail.com',
            'password': 'password'
        }
        response = cls.c.post(
            '/api/login/',
            data=cls.login_context
        )
        cls.access_token = response.data['tokens']['access_token']

    def test_new_superuser(self):
        """
        관리자 계정 생성 TEST
        """
        self.assertEqual(self.super_user.email, 'testadmin@gmail.com')
        self.assertEqual(self.super_user.user_name, 'testsuper')
        self.assertTrue(self.super_user.is_superuser)
        self.assertTrue(self.super_user.is_staff)
        self.assertTrue(self.super_user.is_active)
        self.assertEqual(str(self.super_user.user_name), 'testsuper')

    def test_new_user(self):
        """
        일반 유저 생성 TEST
        """
        self.assertEqual(self.user.email, 'user@gmail.com')
        self.assertEqual(self.user.user_name, 'testuser')
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertEqual(str(self.user.user_name), 'testuser')

    def test_login_user(self):
        """
        로그인 TEST
        """
        response = self.c.post(
            '/api/login/',
            data=self.login_context
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """
        회원 탈퇴 TEST
        """
        response = self.c.delete(
            '/api/users/',
            {'email': 'user@gmail.com'},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
