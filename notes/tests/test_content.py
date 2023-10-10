from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='new_note',
        )

    def test_note_in_list(self):
        users_count = (
            (self.author, 1),
            (self.reader, 0),
        )
        for user, expected_count in users_count:
            self.client.force_login(user)
            with self.subTest(user=user, expected_count=expected_count):
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                notes_count = len(object_list)
                self.assertEqual(notes_count, expected_count)


class TestDetailPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='new_note',
        )

    def test_author_has_form(self):
        url_names = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in url_names:
            self.client.force_login(self.author)
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
