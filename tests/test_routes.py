# news/tests/test_routes.py
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from news.models import News, Comment

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Заголовок', text='текст')
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Хуй простой')
        cls.comment = Comment.objects.create(
            news=cls.news, author=cls.author, text='lol'
        )

    def test_pages_availability(self):
        urls = (
            ('news:home', None),
            ('news:detail', (self.news.pk,)),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_comment_edit_and_delete(self):
        user_status = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in user_status:
            self.client.force_login(user)
            for name in ('news:edit', 'news:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.comment.id,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_anonymous(self):
        login_url = reverse('users:login')
        for name in ('news:edit', 'news:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.comment.id,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
