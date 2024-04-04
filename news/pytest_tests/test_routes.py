from django.urls import reverse
from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name_url, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('news_args')),
    ),
)
def test_pages_availability_for_anonymous_user(client, args, name_url):
    url = reverse(name_url, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, excepted_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'name_url',
    (
        'news:edit',
        'news:delete',
    ),
)
def test_comment_availability_for_different_users(
    parametrized_client, name_url, comment_args, excepted_status
):
    url = reverse(name_url, args=comment_args)
    response = parametrized_client.get(url)
    assert response.status_code == excepted_status


@pytest.mark.parametrize(
    'name_url',
    (
        'news:delete',
        'news:edit',
    ),
)
def test_comment_redirects_for_anonymous_user(client, name_url, comment_args):
    login_url = reverse('users:login')
    url = reverse(name_url, args=comment_args)
    excepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, excepted_url)
