from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import MyUser, UserCheck
from django.urls import reverse
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required


def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            login(request, user)
            return redirect(reverse('index'))

    form = UserRegisterForm()

    return render(request, 'myuser/register.html', context={'form': form})


def user_login_view(request):

    if request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            login(request, user)

            return redirect('index')
    form = UserLoginForm()

    return render(request, 'myuser/login.html', context={'form': form})


@login_required(login_url='/user/login/')
def user_logout_view(request):
    logout(request)
    return redirect('index')




# def user_register_view(request):
#
#     if request.method == 'POST':
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#
#         subject = 'Your code!'
#         text_code = str(randint(1, 99))
#
#         user = UserCheck.objects.create(
#             email=email,
#             username=username,
#             password=password,
#             code=text_code,
#         )
#         receiver = request.session['email'] = email
#
#         try:
#             send_mail(subject, text_code, 'eldarakashka@gmail.com', [receiver])
#         except:
#             user.delete()
#             return HttpResponse('fail!')
#
#         return render(request, 'myuser/add_code.html')
#
#
# def add_code(request):
#
#     if request.method == 'POST':
#         email = request.session.pop('email')
#         user = UserCheck.objects.get(email=email)
#
#         if str(user.code) == str(request.POST['code']):
#             user.delete()
#             user = MyUser.objects.create_user(
#                 email=user.email,
#                 username=user.username,
#                 password=user.password
#             )
#
#             login(request, user)
#             return redirect('/admin/')
#
#         user.delete()
#         return HttpResponse('Your code is not valid')




