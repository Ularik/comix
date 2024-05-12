import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "django-insecure-!231jojsgkdl)uf#&vgh26jkjak1xegdkt_6khszkl"

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '92.63.179.161']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'comix',  # Имя вашей базы данных
        'USER': 'ular',  # Имя вашего пользователя
        'PASSWORD': 'admin',  # Ваш пароль
        'HOST': 'localhost',  # Хост, на котором работает PostgreSQL
        'PORT': '',  # Порт (по умолчанию 5432)
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')