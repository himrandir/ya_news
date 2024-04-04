from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from news.forms import CommentForm
from news.models import News, Comment

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        all_news = []
        today = datetime.today()
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
            # News.objects.create(
            #     title=f'Новость {index}', text='Очередная новость'
            # )
            news = News(
                title=f'Новость {index}',
                text='Очередная новость',
                date=today - timedelta(days=index),
            )
            all_news.append(news)
        News.objects.bulk_create(all_news)

    def testHomePage(self):
        response = self.client.get(settings.HOME_URL)
        object_list = response.context['object_list']
        self.assertEqual(object_list.count(), settings.NEWS_COUNT_ON_HOME_PAGE)

    def testNewsOrder(self):
        response = self.client.get(settings.HOME_URL)
        object_list = response.context['object_list']
        all_dates = [news.date for news in object_list]
        dates_sorted = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, dates_sorted)


class TestDetailPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='Некая новость', text='Текст какой-то'
        )
        cls.detail_url = reverse('news:detail', args=(cls.news.id,))
        cls.author = User.objects.create(username='Некто')
        now = timezone.now()
        for index in range(10):
            comment = Comment.objects.create(
                news=cls.news, author=cls.author, text=f'lol {index}'
            )
            comment.created = now + timedelta(days=index)
            comment.save()

    def testCommentsOrder(self):
        response = self.client.get(self.detail_url)
        self.assertIn('news', response.context)
        news = response.context['news']
        comments = news.comment_set.all()
        all_timestamps = [comment.created for comment in comments]
        sorted_timestamps = sorted(all_timestamps)
        self.assertEqual(all_timestamps, sorted_timestamps)

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CommentForm)
