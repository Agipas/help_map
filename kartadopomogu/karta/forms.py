from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from captcha.fields import CaptchaField

from .models import *


# class PointForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['cat'].empty_label = "Категорія не вибрана"
#
#     class Meta:
#         model = Point
#         fields = ['title', 'slug', 'content', 'is_published', 'cat']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-input'}),
#             'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
#         }
#     # custom validator def clean_*FIELD*():
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if len(title) > 200:
#             raise ValidationError('Длина превышает 200 символов')
#         return title


# class PointFullForm(PointForm): #extending form
#     images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#
#     class Meta(PointForm.Meta):
#         fields = PointForm.Meta.fields + ['images', ]


class PointForm(forms.Form):
    title = forms.CharField(label='Назва',
                            max_length=255)
    cat = forms.ModelChoiceField(label='Категорія',
                                 queryset=Category.objects.all(),
                                 required=True)
    photo = forms.ImageField(label='Основне фото')
    adds_photo = forms.FileField(label='Додаткові фотографії',
                                 widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 required=False)
    point_url = forms.CharField(label='Посилання на збір',
                                max_length=255)
    content = forms.CharField(label='Інформація',
                              widget=forms.Textarea)


class ContactForm(forms.Form):
    name = forms.CharField(label='Name',
                           max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
