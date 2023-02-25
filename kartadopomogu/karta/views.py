from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.shortcuts import render
from .models import Point, Image, Category
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
import datetime
from django.db.models import Q
from django.views.generic import ListView
from .utils import *

# Create your views here.

# def addNoteView(request):
#     if request.method == "POST" and request.is_ajax():
#         form = PointFullForm(request.POST or None, request.FILES or None)
#         files = request.FILES.getlist('images')
#         if form.is_valid():
#             note_created = True
#             user = request.user
#             title = form.cleaned_data['title']
#             note_id = form.cleaned_data['note_id']
#             text = form.cleaned_data['text']
#             tags = tagsInDic(form.cleaned_data['tags'].strip())
#             tags_dic = tags.copy()
#             if not note_id:
#                 note_obj = Point.objects.create(user=user,title=title,text=text) #create will create as well as save too in db.
#                 for k in tags.keys():
#                     tag_obj, created = Category.objects.get_or_create(name=k)
#                     note_obj.tags.add(tag_obj) #it won't add duplicated as stated in django docs
#             else:
#                 # handling all cases of the tags
#                 note_obj = Point.objects.get(id=note_id)
#                 for t in note_obj.tags.all():
#                     if t.name not in tags_dic:
#                         note_obj.tags.remove(t)
#                     else: #deleting pre-existing element so that we could know what's new tags are
#                         del tags_dic[t.name]
#                 for k,v in tags_dic.items():
#                     tag_obj, created = Tag.objects.get_or_create(name=k)
#                     note_obj.tags.add(tag_obj)
#                 note_created = False
#             for f in files:
#                 Image.objects.create(note=note_obj,image=f)
#             note_obj.title = title
#             note_obj.text = text
#             note_obj.save() #last_modified field won't update on chaning other model field, save() trigger change
#             return getNoteResponseData(note_obj,tags,note_created)
#         else:
#             print("Form invalid, see below error msg")
#             print(form.errors)
#     # if GET method form, or anything wrong then we will create blank form
#     else:
#         form = PointFullForm()
#     return HttpResponseRedirect('/')
#
#
# def getNoteResponseData(note_obj, tags, note_created):
#     date = datetime.datetime.now().strftime('%B') + " " + datetime.datetime.now().strftime('%d')+", "+datetime.datetime.now().strftime('%Y')
#     note_obj.refresh_from_db()
#     response_data = {
#             "id": note_obj.id,
#             "title": note_obj.title,
#             "text": note_obj.text,
#             "tags": tags,
#             "last_mod": date,
#             "note_created": note_created
#             }
#     return JsonResponse(response_data)
#
# def tagsInDic(tags):
#     """Convert comma separated tags into dictionary"""
#     last_ind = 0
#     res = {}
#     for i, c in enumerate(tags):
#         if c == ',':
#             res[tags[last_ind:i]] = 1
#             last_ind = i + 1
#     res[tags[last_ind:]] = 1
#     return res


class PointPage(DataMixin, ListView):
    model = Point
    template_name = 'karta/index.html'
    context_object_name = 'points'
    # extra_context = {'title': 'Main Page'} only for static

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна Сторінка')
        return {**context, **c_def}

    def get_queryset(self):
        return Point.objects.filter(is_published=True).select_related('cat')


class ShowPoint(DataMixin, DetailView):
    model = Point
    template_name = 'karta/index.html'
    context_object_name = 'point'
    slug_url_kwarg = 'point_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.filter(point=context["point"].id)
        context["images"] = images
        c_def = self.get_user_context(title=self.kwargs['point_slug'].capitalize())
        return {**context, **c_def}


def contact(request):
    # додати меню з контексту
    return render(request, 'karta/about.html', {'title': 'uss', 'menu': menu})


def about(request):
    # додати меню з контексту
    return render(request, 'karta/about.html', {'title': 'uss', 'menu': menu})
