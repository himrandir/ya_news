import pytest

from django.test.client import Client
from notes.models import Note


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
def note(author):
    note1 = Note.objects.create(
        title='title',
        text='text',
        slug='note-slug',
        author=author,
    )
    return note1


@pytest.fixture
def note_args(note):
    return (note.slug,)


@pytest.fixture
def form_data():
    return {'title': 'new title', 'text': 'new text', 'slug': 'new-slug'}
