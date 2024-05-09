import rarfile
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Comix, Likes, Bookmarks, Comments, Rating, Genre, Posters
from .forms import ComicsCreateForm
from django.views.generic import ListView
from .filters import ComixFilter
from django.contrib.auth import get_user_model
from .utils import is_exist
from functools import partial
import base64
import io
from django.core.cache import cache
import zipfile
from PIL import Image

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
    filterset_class = ComixFilter

    def get_queryset(self):
        sort_param = self.request.GET.get('sort')
        if sort_param == 'bestsellers':
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

        self.filterset = ComixFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter'] = self.filterset

        return context


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
                print('LIKE!')
                like = get_exist_object('comix_like')
                print(like)
                if not like:
                    Likes.objects.create(user=user, comix=comix)
                else:
                    like.delete()

            if 'comment' in request.POST:
                print('COMMENT!')
                Comments.objects.create(user=user, text=request.POST['comment'], comix=comix)

            if 'comix_bookmark' in request.POST:
                print('BOOKMARK!')
                bookmark = get_exist_object('comix_bookmark')
                if not bookmark:
                    Bookmarks.objects.create(user=user, comix=comix)
                else:
                    bookmark.delete()

            if 'grade' in request.POST:
                print('GRADE!')
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
    page_num = int(request.GET.get('page', 0))  # get page_num for comix
    comix = Comix.objects.get(pk=pk)
    file_path = comix.comix_file.url  # get path of comix_file.cbr
    image_name = f'{comix.title}p{page_num}'
    print(file_path)

    if image_name in cache:
        image_base64 = cache.get(image_name)
        return render(request, 'comix/image.html',
                      context={'image_page': f'data:image/jpeg;base64,{image_base64}'})

    if comix.pages:
        if page_num < 0 or page_num > comix.pages:
            return render(request, 'comix/image.html', context={'the_end': '1'})

    open_comix_file = rarfile.RarFile
    if file_path.endswith('cbz'):
        open_comix_file = zipfile.ZipFile

    with open_comix_file(rf'.{file_path}', 'r') as archive:  # extract comix_file.cbr
        name_list = archive.namelist()  # get name of every page in comix
        count = -1
        for image_name in name_list:
            if image_name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                count += 1
                with archive.open(image_name) as page_content:
                    image = Image.open(page_content)  # open image with Pillow
                    image_bytes = io.BytesIO()  # open buffer in byte
                    image.save(image_bytes, format='JPEG')  # save image in buffer: image_bytes in JPEG format
                    image_bytes = image_bytes.getvalue()  # get value for buffer in bytes format
                    image_base64 = base64.b64encode(image_bytes).decode(
                        'utf-8')  # base64 get bytes and return string code
                    image_name = f'{comix.title}p{count}'
                    cache.set(image_name, image_base64, 30 * 60)
        if not comix.pages:
            comix.pages = count
            print('Save pages!')
            comix.save()

    image_name = f'{comix.title}p{page_num}'
    if image_name in cache:
        image_base64 = cache.get(image_name)
        data = {'image_page': f'data:image/jpeg;base64,{image_base64}'}
    else:
        data = {'page_not_found': '1'}

    return render(request, 'comix/image.html', context=data)


# def catalog(request):
#     populate = Comix.objects.order_by('-watches')[:15]
#     populate_pk = populate.values_list('id', flat=True)
#     bestsellers = Comix.objects.filter(pk__in=populate_pk, common_grade__gte=7)
#     updates_nearly = Comix.objects.order_by('-updated_date')[:15]
#
#     data = {
#         'populate': populate,
#         'bestsellers': bestsellers,
#         'updates_nearly': updates_nearly
#     }
#     for genre in Genre.objects.all():
#         stack_of_comics = Comix.objects.filter(genre=genre)
#         data['genres'] = data.get('genres', []).append(stack_of_comics)
#
#     return render(request, 'comix/categories.html', context=data)


def contact(request):
    return HttpResponse('Bound')


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


def about(request):
    return render(request, 'comix/about.html', {'title': 'about page'})


def page_not_found(request):
    return HttpResponse('Page_not_found')
