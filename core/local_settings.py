import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = "django-insecure-!e$nk5dios1gqs)uf#&vgh26hp7=il@$%xx1xegdkt_6khszkl"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'comix',  # Имя вашей базы данных
        'USER': 'ular',  # Имя вашего пользователя
        'PASSWORD': 'admin',  # Ваш пароль
        'HOST': 'localhost',  # Хост, на котором работает PostgreSQL
        'PORT': '5432',  # Порт (по умолчанию 5432)
    }
}


STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]

