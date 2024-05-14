from . import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name='index'),
    path('comics_list/', views.ComicsListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('categories/', views.category_view, name='categories'),
    path('create/', views.create_comics_view, name='create'),
    path('open_file/<int:pk>/', views.open_file, name='open_file')
]
