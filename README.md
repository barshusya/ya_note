# YaNote

## About ⭐

YaNote - an electronic notebook for those who don't want to forget anything and therefore write everything down.

The purpose of this project is to prepare tests for checking content, logic and routes for django-based website.

## Test plan 📋

### test_content 📄

[//]: # (тесты, касающиеся отображения контента. Какие данные на каких страницах отображаются, какие при этом используются шаблоны, как работает пагинатор)

- [x] The individual note is passed to the notes list page in the object_list list within the context dictionary;
- [x] Notes from one user are not included in the list of notes for another user;
- [x] The creation and editing pages for a note receive forms.

### test_logic 💡

[//]: # (тестирование бизнес-логики приложения. Как обрабатываются те или иные формы, разрешено ли создание объектов с неуникальными полями, как работает специфичная логика конкретного приложения)

- [x] A logged-in user can create a note, while an anonymous user cannot;
- [x] It is not possible to create two notes with the same slug;
- [x] If the slug is not filled in when creating a note, it is automatically generated using the pytils.translit.slugify function;
- [x] A user can edit and delete their own notes, but cannot edit or delete notes from others.

### test_routes 📍

[//]: # (тесты доступности конкретных эндпоинтов, проверка редиректов, кодов ответа, которые возвращают страницы, тестирование доступа для авторизованных или анонимных пользователей)

- [x] The main page is available to anonymous users;
- [x] Authenticated users have access to the notes/ page, which contains a list of notes, the done/ page for successful note additions, and the add/ page for adding a new note;
- [x] Pages for individual note viewing, note deletion, and note editing are only accessible to the note's author. If another user tries to access these pages, a 404 error will be returned;
- [x] When attempting to access the notes list page, the successful note addition page, the note addition page, the individual note page, or the note editing/deletion pages, an anonymous user will be redirected to the login page;
- [x] User registration, account login, and logout pages are accessible to all users.

### not for tests 🚫

- users registration
- admin zone
- HTML-templates