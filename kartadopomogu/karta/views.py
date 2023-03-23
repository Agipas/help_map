from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PointForm, PointUpdateForm, ImageUpdateForm
from .utils import *


class PointPage(DataMixin, ListView):
    model = Point
    template_name = 'karta/index.html'
    context_object_name = 'points'
    extra_context = {'title': 'Головна Сторінка'}
    queryset = Point.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cats"] = {point.cat for point in Point.objects.filter(is_published=True).select_related('cat')}
        c_def = self.get_user_context()
        return {**context, **c_def}


class PointCategory(PointPage):
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        con = {
            'title': 'Category ' + self.kwargs['cat_slug'].capitalize(),
            'cat_selected': context['points'][0].cat_id,
        }
        c_def = self.get_user_context(**con)
        return {**context, **c_def}

    def get_queryset(self):
        return Point.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


@method_decorator(login_required, name='dispatch')
class UsersPointPage(PointPage):
    extra_context = {'title': 'Ваші Записи',
                     'user_page': True}

    def get_queryset(self):
        return Point.objects.filter(author=self.request.user).select_related('cat')


class ShowPoint(DataMixin, DetailView):
    model = Point
    template_name = 'karta/info.html'
    context_object_name = 'point'
    slug_url_kwarg = 'point_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.filter(point=context["point"].id)
        authors_points = Point.objects.filter(author=context["point"].author)
        context["images"] = images
        context["authors_points"] = authors_points
        c_def = self.get_user_context(title=self.kwargs['point_slug'].capitalize())
        return {**context, **c_def}


@method_decorator(login_required, name='dispatch')
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
        form = self.get_form(self.form_class)
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


@method_decorator(login_required, name='dispatch')
class UpdatePoint(DataMixin, View):
    title = 'Редагувати Допомогу'
    template_name = 'karta/updatepage.html'

    @staticmethod
    def get_data(point_slug):
        point = get_object_or_404(Point, slug__iexact=point_slug)
        images = Image.objects.filter(point=point)
        adds_photo = [ImageUpdateForm(instance=image, prefix=image.pk) for image in images]
        return point, images, adds_photo

    def get_context(self, point_form, point, adds_photo):
        context = {'form': point_form,
                   'point': point,
                   'title': self.title,
                   'adds_photo': adds_photo}
        user_context = self.get_user_context()
        return {**context, **user_context}

    def get(self, request, point_slug):
        point, images, adds_photo = self.get_data(point_slug)
        if point.author != request.user:
            return redirect(reverse('index'))
        point_form = PointUpdateForm(instance=point)
        context = self.get_context(point_form, point, adds_photo)
        return render(request, self.template_name, context=context)

    def post(self, request, point_slug):
        point, images, adds_photo = self.get_data(point_slug)
        if point.author != request.user:
            return redirect(reverse('index'))
        files = request.FILES.getlist('adds_photo')
        point_form = PointUpdateForm(request.POST, instance=point)
        imgs_to_delete = [int(img.split('-')[0]) for img in request.POST.keys() if 'image-clear' in img]
        if point_form.is_valid():
            new_point = point_form.save()
            Image.objects.filter(id__in=imgs_to_delete).delete()
            for f in files:
                Image.objects.create(image=f, point=point)
            return redirect(new_point)
        context = self.get_context(point_form, point, adds_photo)
        return render(request, self.template_name, context=context)


@login_required
def contact(request):
    context = {'title': 'Contact'}
    context = get_user_context(request.user, context)
    return render(request, 'karta/about.html', context)


@login_required
def about(request):
    context = {'title': 'About'}
    context = get_user_context(request.user, context)
    return render(request, 'karta/about.html', context)


@login_required
def delete_point(request, point_slug):
    point = Point.objects.get(slug=point_slug)
    if point.author != request.user:
        return HttpResponseRedirect(reverse('index'))
    point.delete()
    return HttpResponseRedirect(reverse('index'))


def location_map(request):
    locations = Point.objects.all()
    return render(request, 'location_map.html', {'locations': locations})
