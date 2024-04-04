from django.urls import reverse
import pytest
from notes.forms import NoteForm

# def test_note_in_list_for_author(note, author_client):
#     url = reverse('notes:list')
#     response = author_client.get(url)
#     object_list = response.context['object_list']
#     assert note in object_list


# def test_note_in_list_for_another_user(note, not_author_client):
#     url = reverse('notes:list')
#     response = not_author_client.get(url)
#     object_list = response.context['object_list']
#     assert note not in object_list


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False),
    ),
)
def test_note_in_list_for_different_users(
    parametrized_client, note, note_in_list
):
    url = reverse('notes:list')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) == note_in_list


# def test_create_note_page_contains_form(author_client):
#     url = reverse('notes:add')
#     response = author_client.get(url)
#     assert 'form' in response.context
#     assert isinstance(response.context['form'], NoteForm)


# def test_edit_note_page_contains_form(author_client, note_args):
#     url = reverse('notes:edit', args=note_args)
#     response = author_client.get(url)
#     assert 'form' in response.context
#     assert isinstance(response.context['form'], NoteForm)


@pytest.mark.parametrize(
    'name, args',
    (('notes:add', None), ('notes:edit', pytest.lazy_fixture('note_args'))),
)
def test_pages_contains_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)
