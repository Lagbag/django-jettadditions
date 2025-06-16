"""
Инструкция по настройке Django-проекта
TODO: Настройка Django-проекта

Создание проекта  

Выполните команду для создания нового Django-проекта, заменив <ВАША_ФАМИЛИЯ> на вашу фамилию (без символов <>, например, Ivanov):  django-admin startproject <ВАША_ФАМИЛИЯ>




Переход в директорию проекта  

Перейдите в папку проекта, созданную на предыдущем шаге:  cd <ВАША_ФАМИЛИЯ>




Создание приложения  

Создайте новое Django-приложение, придумав уникальное название (например, myapp):  django-admin startapp <НАЗВАНИЕ_ПРИЛОЖЕНИЯ>




Копирование Python-файлов  

Скопируйте все файлы с расширением .py из библиотеки (например, из django_jettadditions) в папку приложения, созданного на шаге 3 (<НАЗВАНИЕ_ПРИЛОЖЕНИЯ>).


Создание папки templates  

В корне проекта (на одном уровне с папками <ВАША_ФАМИЛИЯ> и <НАЗВАНИЕ_ПРИЛОЖЕНИЯ>) создайте папку templates.


Копирование шаблонов  

Скопируйте файлы шаблонов (например, home.html, login.html) из библиотеки templates/django_jettadditions в созданную папку templates.


Обновление путей в views.py  

Откройте файл <НАЗВАНИЕ_ПРИЛОЖЕНИЯ>/views.py.  
Найдите строки, где указаны пути к шаблонам (например, django_jettadditions/home.html).  
Замените их на прямые имена файлов, например:  return render(request, 'home.html')

или  return render(request, 'login.html')


Убедитесь, что все упоминания django_jettadditions/ удалены.




Обновление INSTALLED_APPS в settings.py  

Откройте файл <ВАША_ФАМИЛИЯ>/settings.py.  
В список INSTALLED_APPS добавьте название вашего приложения после последней запятой:  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<НАЗВАНИЕ_ПРИЛОЖЕНИЯ>',
]




Настройка ROOT_URLCONF и AUTH_USER_MODEL  

В том же файле settings.py убедитесь, что:  ROOT_URLCONF = '<ВАША_ФАМИЛИЯ>.urls'
AUTH_USER_MODEL = '<НАЗВАНИЕ_ПРИЛОЖЕНИЯ>.CustomUser'


Замените <ВАША_ФАМИЛИЯ> и <НАЗВАНИЕ_ПРИЛОЖЕНИЯ> на ваши значения (например, Ivanov и myapp).




Обновление TEMPLATES в settings.py  

Замените секцию TEMPLATES на следующую конфигурацию:  TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]




Настройка базы данных  

В settings.py найдите секцию DATABASES и замените её, указав параметры вашей базы данных PostgreSQL:  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<ИМЯ_БАЗЫ_ДАННЫХ>',
        'USER': '<ИМЯ_ПОЛЬЗОВАТЕЛЯ_БД>',
        'PASSWORD': '<ПАРОЛЬ_БД>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


Замените <ИМЯ_БАЗЫ_ДАННЫХ>, <ИМЯ_ПОЛЬЗОВАТЕЛЯ_БД> и <ПАРОЛЬ_БД> на значения из вашей настройки PostgreSQL в pgAdmin4.




Обновление urls.py проекта  

Откройте файл <ВАША_ФАМИЛИЯ>/urls.py.  
Замените его содержимое на:  from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('<НАЗВАНИЕ_ПРИЛОЖЕНИЯ>.urls')),
]




Обновление urls.py приложения  

В папке <НАЗВАНИЕ_ПРИЛОЖЕНИЯ> откройте файл urls.py.  
Найдите строку:  from django_jettadditions import views


Замените её на:  from <НАЗВАНИЕ_ПРИЛОЖЕНИЯ> import views




Обновление apps.py  

В папке <НАЗВАНИЕ_ПРИЛОЖЕНИЯ> откройте файл apps.py.  
Убедитесь, что он выглядит так:  from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '<НАЗВАНИЕ_ПРИЛОЖЕНИЯ>'


Замените <НАЗВАНИЕ_ПРИЛОЖЕНИЯ> на название вашего приложения.




Запуск сервера  

Выполните миграции для настройки базы данных:  python manage.py makemigrations
python manage.py migrate


Запустите сервер разработки:  python manage.py runserver


Откройте браузер и перейдите по адресу http://localhost:8000/ для проверки.
"""

