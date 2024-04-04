from datetime import datetime, timedelta
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
import pytest
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news_list():
    all_news = []
    today = datetime.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость {index}',
            text='Очередная новость',
            date=today - timedelta(days=index),
        )
        all_news.append(news)
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def news():
    news = News.objects.create(
        title='title',
        text='text',
    )
    return news


@pytest.fixture
def news_url(news):
    url = reverse('news:detail', args=(news.id,))
    return url


@pytest.fixture
def comment_list(news, author):
    all_comments = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        comment = Comment(
            text=f'Комментарий {index}',
            author=author,
            news=news,
        )
        all_comments.append(comment)
    Comment.objects.bulk_create(all_comments)
    return all_comments


@pytest.fixture
def news_args(news):
    return (news.id,)


@pytest.fixture
def comment_by_author(author, news):
    comment = Comment.objects.create(
        news=news, author=author, text='Под столом'
    )
    return comment


@pytest.fixture
def comment_by_not_author(not_author, news):
    comment = Comment.objects.create(
        news=news, author=not_author, text='Не вижу ничего смешного'
    )
    return comment


@pytest.fixture
def comment_args(comment_by_author):
    return (comment_by_author.id,)


@pytest.fixture
def form_data(news):
    return {'text': 'new-text', 'news': news}
