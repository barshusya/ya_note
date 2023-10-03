# YaNote

## About ⭐

YaNote - an electronic notebook for those who don't want to forget anything and therefore write everything down.

The purpose of this project is to prepare tests for checking content, logic and routes for django-based website.

## Test plan 📋

### test_content 📄

[//]: # (тесты, касающиеся отображения контента. Какие данные на каких страницах отображаются, какие при этом используются шаблоны, как работает пагинатор)

- [ ] Количество заметок в списке заметок не более 10
- [ ] Заметки отсортированы от самой свежей к самой старой. Свежие заметки в начале списка
- [ ] Анонимному пользователю недоступна страница создания заметки, а авторизованному доступна

### test_logic 🧐

[//]: # (тестирование бизнес-логики приложения. Как обрабатываются те или иные формы, разрешено ли создание объектов с неуникальными полями, как работает специфичная логика конкретного приложения)

- [ ] Авторизованный пользователь может создать заметку
- [ ] Авторизованный пользователь может редактировать и удалять заметки
- [ ] Анонимный пользователь не может создать заметку

### test_routes 🚲

[//]: # (тесты доступности конкретных эндпоинтов, проверка редиректов, кодов ответа, которые возвращают страницы, тестирование доступа для авторизованных или анонимных пользователей)

- [ ] Главная страница доступна анонимному пользователю
- [ ] Страница отдельной заметки доступна только автору
- [ ] Страница редактирования и удаления записи доступны автору
- [ ] При попытке перейти на страницу редактирования или удаления чужой заметки пользователь перенаправляется на страницу авторизации
- [ ] Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны анонимным пользователям
- [ ] При попытке открыть несуществующую запись вернется ошибка 404
- [ ] При незаполненном поле slug для страницы заметки используется транслитерированное название заметки

### not for tests

- users registration
- admin zone
- HTML-templates