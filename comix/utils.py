import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from .models import Comix, Bookmarks, Likes, Rating


def is_exist(user, comix, model_type):
    dct = {'comix_like': Likes, 'comix_bookmark': Bookmarks, 'grade': Rating}
    record = dct[model_type].objects.filter(user=user, comix=comix).first()
    if record:
        return record


