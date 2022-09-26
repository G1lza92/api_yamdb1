# Групповой роект «API для YaMDb»
## Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка.
Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
## Установка:
### После клонирования репрозитория:
* Установаите виртуальное окружение
```python -m venv venv / python3 -m venv venv```
>
* Активируйте виртуальное окружение
```source venv/Scripts/activate / source venv/bin/activate```
>
* Установите requirements
```pip install -r requirements.txt```
>
* Перейдите в api_yamdb
```cd api_yamdb```
>
* Выполните миграции
```python manage.py migrate```
>
* Запуск сервера
```python manage.py runserver```
>
>
### Загрузка данных и CSV-файлов (./static/data/*.csv) 
```python manage.py load_data```
### Загрузка дынных без вывода в терминал
```python manage.py load_data -v 0```
>
### Пользовательские роли:
* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
* Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
* Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* Суперюзер Django - обладает правами администратора (admin) 
>
### Регистрация нового пользователя:
```(POST) /api/v1/auth/signup/```
#### На email приходит confirmation_code для получения JWT-Token
```
{ 
    "email": "string",
    "username": "string"
}
```
>
### Получение JWT-token:
```(POST) /api/v1/auth/token/```
```
{
    "username": "string",
    "confirmation_code": "string"
}
```
### Более подробная документация со всеми адресами и доступными методами доступны по:
>
## Динамическая документация Swagger - [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
>
## Спецификация ReDoc - [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)