from django import forms
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField

from .models import *


class PointForm(forms.Form):
    title = forms.CharField(label='Назва',
                            max_length=255)
    cat = forms.ModelChoiceField(label='Категорія',
                                 queryset=Category.objects.all(),
                                 required=True)
    photo = forms.ImageField(label='Основне зображення')
    adds_photo = forms.FileField(label='Додаткові зображення',
                                 widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 required=False)
    point_url = forms.CharField(label='Посилання на збір',
                                max_length=255)
    content = forms.CharField(label='Інформація',
                              widget=forms.Textarea)
    is_published = forms.BooleanField(label='Опублікувати?',
                                      widget=forms.CheckboxInput,
                                      required=False)


class PointUpdateForm(forms.ModelForm):
    title = forms.CharField(label='Назва',
                            max_length=255)
    cat = forms.ModelChoiceField(label='Категорія',
                                 queryset=Category.objects.all(),
                                 required=True)
    photo = forms.ImageField(label='Основне зображення')
    point_url = forms.CharField(label='Посилання на збір',
                                max_length=255)
    content = forms.CharField(label='Інформація',
                              widget=forms.Textarea)
    is_published = forms.BooleanField(label='Опублікувати?',
                                      widget=forms.CheckboxInput,
                                      required=False)
    adds_photo = forms.FileField(label='Нові зображення',
                                 widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 required=False)

    class Meta:
        model = Point
        exclude = ['date_created', 'date_created', 'author', 'slug']


class ImageUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='Додаткове зображення', required=False)

    class Meta:
        model = Image
        fields = ['image']


class ContactForm(forms.Form):
    name = forms.CharField(label='Name',
                           max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
