from django.conf import settings
import pytest
from news.forms import CommentForm


@pytest.mark.django_db
def test_count_news_on_home_page(client, news_list):
    response = client.get(settings.HOME_URL)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


# @pytest.mark.parametrize(
#     'name_url, current_list, key',
#     (
#         (settings.HOME_URL, pytest.lazy_fixture('news_list'), 'object_list'),
#         (
#             pytest.lazy_fixture('news_url'),
#             pytest.lazy_fixture('comment_list'),
#             'news',
#         ),
#     ),
# )
# @pytest.mark.django_db
# def test_check_order_news_on_home_page(client, name_url, key, current_list):
#     response = client.get(name_url)
#     print(response.context['object'].comment_set.all())
#     object_list = response.context[key]
#     all_dates = [news.date for news in object_list]
#     dates_sorted = sorted(all_dates, reverse=True)
#     assert all_dates == dates_sorted


@pytest.mark.django_db
def test_check_order_news_on_home_page(client, news_list):
    response = client.get(settings.HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    dates_sorted = sorted(all_dates, reverse=True)
    assert all_dates == dates_sorted


@pytest.mark.django_db
def test_check_order_comments_on_news_page(client, news_url, comment_list):
    response = client.get(news_url)
    object_list = response.context['object'].comment_set.all()
    all_dates = [comment.created for comment in object_list]
    dates_sorted = sorted(all_dates, reverse=False)
    assert all_dates == dates_sorted


@pytest.mark.parametrize(
    'parametrized_client, name_url, form_is_enabled',
    (
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('news_url'),
            True,
        ),
        (
            pytest.lazy_fixture('client'),
            pytest.lazy_fixture('news_url'),
            False,
        ),
    ),
)
@pytest.mark.django_db
def test_pages_contains_form(parametrized_client, name_url, form_is_enabled):
    response = parametrized_client.get(name_url)
    assert ('form' in response.context) == form_is_enabled
    if form_is_enabled:
        assert isinstance(response.context['form'], CommentForm)
