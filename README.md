﻿# Django Справочник пользователей

Этот проект представляет собой веб-приложение на Django для управления справочником пользователей. Приложение позволяет:
- Регистрировать пользователей с дополнительными полями (ФИО, год рождения, пол, фото, статус администратора, кем зарегистрирован).
- Создавать, редактировать и удалять профили пользователей (только для администраторов).
- Просматривать список пользователей и подробности профиля.
- Отображать сводку регистрации с возможностью сортировки по ФИО, кем зарегистрирован и дате регистрации.
- Навигировать между страницами через боковое меню с плавным появлением/исчезанием.

## Функциональность

- **Регистрация пользователя**  
  Пользователь может зарегистрироваться самостоятельно через форму регистрации. При регистрации в профиле поле `registered_by` устанавливается в значение `сам` (если пользователь регистрируется самостоятельно) или — если регистрацию проводит администратор — сохраняется логин администратора.

- **Управление профилями**  
  Администраторы (пользователи с `is_staff=True`) могут создавать, редактировать и удалять профили пользователей через сайт.

- **Сводка регистрации**  
  Отдельная страница отображает таблицу регистрации, в которой видно, какой пользователь кем зарегистрирован и когда, с возможностью сортировки по каждому столбцу.

- **Боковое меню**  
  На страницах реализовано боковое меню с навигацией между «Списком пользователей» и «Таблицей регистрации». Меню плавно появляется/исчезает, а активный пункт подсвечивается.

## Требования

- Python 3.12+
- Django 5.1.6
- Pillow (для работы с изображениями)
- django-widget-tweaks
- python-dotenv

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone <URL_репозитория>
   cd <название_проекта>

2. **Создайте и активируйте виртуальное окружение:**

    ```bash
    python -m venv env
    # Windows:
    env\Scripts\activate
    # Linux/macOS:
    source env/bin/activate
   
3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt

4. **Настройте переменные окружения:**  
    Создайте файл .env в корне проекта и добавьте:

    ```ini
    SECRET_KEY=ваш_секретный_ключ
   
5. **Выполните миграции:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
   
6. **Создайте суперпользователя:**

    ```bash
    python manage.py createsuperuser
   
7. **Запустите сервер разработки:**

    ```bash
    python manage.py runserver
    Откройте http://127.0.0.1:8000/ в браузере.
   
## Структура проекта
- **core – приложение, содержащее:**

models.py – модель UserProfile с дополнительными полями.  
forms.py – формы регистрации (RegistrationForm) и редактирования профиля (UserProfileForm).  
views.py – вьюхи для регистрации, создания, редактирования, удаления, просмотра списка и деталей профилей, а также сводки регистрации.  
templates/core/ – шаблоны для страниц: список пользователей, детали профиля, создание, редактирование, сводка регистрации и подтверждение удаления.  
templatetags/custom_filters.py – кастомные фильтры, например, startswith.  
- **test_app – корневой проект Django (настройки, urls, wsgi).**

## Боковое меню и сортировка
- **Боковое меню:**
Реализовано с помощью CSS и JavaScript. Меню содержит ссылки на «Список пользователей» и «Таблицу регистрации». Активный пункт определяется по URL.

- **Сортировка:**
На странице сводки регистрации добавлены ссылки для сортировки по столбцам (ФИО, кем зарегистрирован, дата регистрации). При клике в URL передаётся параметр sort, который обрабатывается в вьюхе.

## Управление правами администратора
Поле is_admin в модели UserProfile синхронизируется с полем is_staff у связанного объекта User.  
Редактирование прав администратора рекомендуется производить через сайт, так как изменения через админку Django могут не синхронизироваться автоматически.
