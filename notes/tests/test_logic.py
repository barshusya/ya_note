from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_COUNT_CREATED = 1
    NOTE_COUNT_NOT_CREATED = 0

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.url = reverse('notes:add')
        cls.form_data = {
            'title': 'Note title',
            'text': 'Note text',
            'slug': 'note-slug',
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        # Whether new note is not added to DB
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.NOTE_COUNT_NOT_CREATED)

    def test_user_can_create_note(self):
        response = self.auth_user.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        # Whether new note is added to DB
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.NOTE_COUNT_CREATED)
        # Whether the data is saved correctly
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_unique_slug(self):
        self.auth_user.post(self.url, data=self.form_data)
        response = self.auth_user.post(self.url, data=self.form_data)
        warn = self.form_data['slug'] + WARNING
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=warn
        )
        # Whether new note is not created
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.NOTE_COUNT_CREATED)

    def test_empty_slug(self):
        del self.form_data['slug']
        response = self.auth_user.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        # Whether new note is created
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.NOTE_COUNT_CREATED)
        # Whether slug is correctly created from title
        expected_slug = slugify(self.form_data['title'])
        note = Note.objects.get()
        self.assertEqual(note.slug, expected_slug)


class TestNoteEditDelete(TestCase):
    NOTE_TITLE = 'Note title'
    NOTE_TEXT = 'Note text'
    NEW_NOTE_TITLE = 'New note title'
    NEW_NOTE_TEXT = 'New note text'
    NOTE_DELETED = 0
    NOTE_NOT_DELETED = 1

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор комментария')
        cls.auth_author = Client()
        cls.auth_author.force_login(cls.author)
        cls.user = User.objects.create(username='Читатель')
        cls.auth_user = Client()
        cls.auth_user.force_login(cls.user)
        cls.note = Note.objects.create(
            author=cls.author,
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
        )
        cls.edit_url = reverse('notes:edit', args=[cls.note.slug])
        cls.delete_url = reverse('notes:delete', args=[cls.note.slug])
        cls.redirect_url = reverse('notes:success')
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
        }

    def test_author_can_delete_note(self):
        response = self.auth_author.delete(self.delete_url)
        self.assertRedirects(response, self.redirect_url)
        # Whether the note is deleted from DB
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.NOTE_DELETED)

    def test_user_cant_delete_note_of_author(self):
        response = self.auth_user.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # Whether the note is in DB
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.NOTE_NOT_DELETED)

    def test_author_can_edit_note(self):
        self.auth_author.post(self.edit_url, self.form_data)
        # Whether the note is changed
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NEW_NOTE_TITLE)
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_note_of_author(self):
        response = self.auth_user.post(self.edit_url, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # Whether the text is not changed
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NOTE_TITLE)
        self.assertEqual(self.note.text, self.NOTE_TEXT)
