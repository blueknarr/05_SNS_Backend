from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class PostsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
        db = get_user_model()

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

    def test_create_post(self):
        """
        게시글 생성
        """
        response = self.c.post(
            '/api/posts/',
            {
                'title': 'test first posting',
                'content': 'test first post content',
                'tags': '#test,#posting,#content'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 201)
