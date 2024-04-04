from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_author_user_can_create_comment(
    author_client, author, news_url, form_data
):
    response = author_client.post(news_url, data=form_data)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assertRedirects(response, f'{news_url}#comments')
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_url, form_data):
    response = client.post(news_url, data=form_data)
    login_url = reverse('users:login')
    excepted_url = f'{login_url}?next={news_url}'
    assertRedirects(response, excepted_url)
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'parametrized_client, name_url, excepted_status',
    (
        (
            pytest.lazy_fixture('not_author_client'),
            'news:edit',
            HTTPStatus.NOT_FOUND,
        ),
        (
            pytest.lazy_fixture('not_author_client'),
            'news:delete',
            HTTPStatus.NOT_FOUND,
        ),
        (
            pytest.lazy_fixture('author_client'),
            'news:delete',
            HTTPStatus.FOUND,
        ),
        (
            pytest.lazy_fixture('author_client'),
            'news:edit',
            HTTPStatus.OK,
        ),
    ),
)
def test_comment_availability_for_different_users(
    parametrized_client,
    name_url,
    excepted_status,
    comment_args,
):
    url = reverse(name_url, args=comment_args)
    response = parametrized_client.post(url)
    print(response)
    assert response.status_code == excepted_status


def test_user_cant_use_bad_words(author_client, news_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(news_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0
