from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
User = get_user_model()


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username')


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
