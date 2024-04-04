from http import HTTPStatus
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects
from notes.models import Note


def test_home_availability_for_anonymous_user(client):
    url = reverse('notes:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name', ('notes:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name', ('notes:list', 'users:login', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_note_exists(note):
    notes_count = Note.objects.count()
    assert notes_count == 1
    assert note.title == 'title'


@pytest.mark.parametrize(
    'parametrized_client, excepted_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'name', ('notes:detail', 'notes:edit', 'notes:delete')
)
def test_pages_availability_for_different_users(
    parametrized_client, name, note_args, excepted_status
):
    url = reverse(name, args=note_args)
    response = parametrized_client.get(url)
    assert response.status_code == excepted_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture('note_args')),
        ('notes:edit', pytest.lazy_fixture('note_args')),
        ('notes:delete', pytest.lazy_fixture('note_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    excepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, excepted_url)
