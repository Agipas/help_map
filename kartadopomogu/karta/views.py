from django.views.generic import ListView, DetailView, CreateView, FormView
from django.shortcuts import render, redirect

from .forms import PointForm
from .utils import *


class PointPage(DataMixin, ListView):
    model = Point
    template_name = 'karta/index.html'
    context_object_name = 'points'
    extra_context = {'title': 'Головна Сторінка'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}

    def get_queryset(self):
        return Point.objects.filter(is_published=True).select_related('cat')


class UsersPointPage(PointPage):
    extra_context = {'title': 'Ваші Записи'}

    def get_queryset(self):
        return Point.objects.filter(author=self.request.user).select_related('cat')


class ShowPoint(DataMixin, DetailView):
    model = Point
    # template_name = 'karta/point_info.html'
    template_name = 'karta/info.html'
    context_object_name = 'point'
    slug_url_kwarg = 'point_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.filter(point=context["point"].id)
        context["images"] = images
        c_def = self.get_user_context(title=self.kwargs['point_slug'].capitalize())
        return {**context, **c_def}


class CreatePoint(DataMixin, FormView):
    template_name = 'karta/addpage.html'
    form_class = PointForm
    success_url = '/'
    extra_context = {'title': 'Створити Допомогу'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('adds_photo')
        if form.is_valid():
            cleaned_data = form.cleaned_data
            del cleaned_data['adds_photo']
            cleaned_data['author'] = request.user
            cleaned_data['slug'] = cleaned_data['title']
            form = Point(**cleaned_data)
            point = form.save()
            for f in files:
                Image.objects.create(image=f, point=point)
            return redirect(reverse('point_info', kwargs={'point_slug': point.slug}))
        else:
            return self.form_invalid(form)


def contact(request):
    context = {'title': 'Contact'}
    context = get_user_context(request.user, context)
    return render(request, 'karta/about.html', context)


def about(request):
    context = {'title': 'About'}
    context = get_user_context(request.user, context)
    return render(request, 'karta/about.html', context)
