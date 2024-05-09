from django import forms
from .models import Comix


class ComicsCreateForm(forms.ModelForm):
    class Meta:
        model = Comix
        fields = (
            'title',
            'description',
            'chapters',
            'pages',
            'genre',
            'comix_file',
            'image'
        )
