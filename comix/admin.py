from django.contrib import admin
from .models import Comix, Genre, Bookmarks, Likes, Comments, Rating, Posters

admin.site.register(Likes)
admin.site.register(Bookmarks)
admin.site.register(Comix)
admin.site.register(Genre)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(Posters)


