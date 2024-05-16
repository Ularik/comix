import os
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Comix, Likes, Bookmarks, Comments, Rating, Genre
from .forms import ComicsCreateForm
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .utils import is_exist
from functools import partial
from django.http import JsonResponse

User = get_user_model()


def index(request):

    sort_param = request.GET.get('sort')
    comics = Comix.objects.all() if not sort_param else Comix.objects.order_by(sort_param)
    data = {
        'comics': comics,
    }

    if request.user.is_authenticated:
        bookmarks = request.user.bookmarks.values_list('comix__pk', flat=True)
        data['bookmarks'] = bookmarks

        if request.method == 'POST':
            if 'bookmark' in request.POST:
                comix_id = request.POST['bookmark'],
                bookmark = Bookmarks.objects.filter(
                    user=request.user,
                    comix__pk=comix_id[0]
                ).first()
                if not bookmark:
                    comix = Comix.objects.get(pk=comix_id[0])
                    Bookmarks.objects.create(user=request.user, comix=comix)
                else:
                    bookmark.delete()
            return redirect('index')

    return render(request, 'comix/index.html', context=data)


class ComicsListView(ListView):
    model = Comix
    template_name = 'comix/comics-list.html'
    context_object_name = 'comix'

    def get_queryset(self):
        sort_param = self.request.GET.get('sort')
        search_name = self.request.GET.get('search')
        if search_name:
            queryset = Comix.objects.filter(title__icontains=search_name)
        elif sort_param == 'bestsellers':
            best_watches = Comix.objects.order_by('-watches').values_list('id', flat=True)[:5]
            queryset = Comix.objects.filter(pk__in=best_watches, common_grade__gte=7)
        else:
            genre_id = self.request.GET.get('genre')
            if genre_id and sort_param:                                           # sort_param [?sort='-watches']
                queryset = Comix.objects.filter(genre__pk=genre_id[0]).order_by(sort_param)
            elif sort_param:
                queryset = Comix.objects.order_by(sort_param)
            elif genre_id:
                queryset = Comix.objects.filter(genre__pk=genre_id[0])
            if not (genre_id or sort_param):
                queryset = super().get_queryset()

            return queryset


def category_view(request):
    genres = Genre.objects.all()
    return render(request, 'comix/comix_categories.html', context={'genres': genres})


def detail(request, pk):
    comix = Comix.objects.filter(pk=pk).first()
    user = request.user
    comments = Comments.objects.filter(comix__pk=pk)

    if request.method == 'POST':

        if user.is_authenticated:

            '''is_exist get user and comix and return 1 record from models(Likes, Bookmarks, Rating)'''

            get_exist_object = partial(is_exist, user, comix)  # partial = is_exist(user, comix, x)
            if 'comix_like' in request.POST:
                like = get_exist_object('comix_like')
                if not like:
                    Likes.objects.create(user=user, comix=comix)
                else:
                    like.delete()

            if 'comment' in request.POST:
                Comments.objects.create(user=user, text=request.POST['comment'], comix=comix)

            if 'comix_bookmark' in request.POST:
                bookmark = get_exist_object('comix_bookmark')
                if not bookmark:
                    Bookmarks.objects.create(user=user, comix=comix)
                else:
                    bookmark.delete()

            if 'grade' in request.POST:
                grade = get_exist_object('grade')
                if not grade:
                    Rating.objects.create(user=user, comix=comix, grade=request.POST['grade'])
                else:
                    grade.grade = request.POST['grade']
                    grade.save()
                all_grades = Rating.objects.values_list('grade', flat=True)
                comix.common_grade = sum(all_grades) / len(all_grades)
                comix.save()

            return redirect(reverse('detail', kwargs={'pk': pk}))

        return redirect('register')

    data = {
        'comix': comix,
        'request': request,
        'comments': comments
    }

    if user.is_authenticated:
        comix_like = user.favorites.filter(comix=pk).first()    # search is this comix have liked by user
        comix_bookmark = user.bookmarks.filter(comix=pk).first()    # search is this comix have marked by user
        data['comix_bookmark'] = bool(comix_bookmark)
        data['comix_like'] = bool(comix_like)

    comix.watches += 1
    comix.save()

    return render(request, 'comix/detail.html', context=data)


def open_file(request, pk):
    page_num = int(request.GET.get('page', 0))     # get page_num for comix
    comix = Comix.objects.get(pk=pk)

    if page_num < 0 or page_num > comix.pages:
        return render(request, 'comix/image.html', context={'the_end': '1'})

    name_page = comix.comix_pages[page_num]
    image = os.path.join(settings.STATIC_URL, 'extract_comix/', comix.title, name_page)
    return render(request, 'comix/image.html', context={'image': image})


@user_passes_test(lambda u: u.is_authenticated and u.is_admin, login_url='/comix/index/')
def create_comics_view(request):
    not_valid = False
    if request.method == 'POST':
        form = ComicsCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
        not_valid = True

    form = ComicsCreateForm()

    return render(request, 'comix/comics-create.html', context={'form': form, 'not_valid': not_valid})

