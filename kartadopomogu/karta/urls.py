from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path("add/", addNoteView, name='add_note'),
    path("", PointPage.as_view(), name='index'),
    path("new_point/", PointPage.as_view(), name='add_point'),
    path("point-info/<slug:point_slug>", ShowPoint.as_view(), name='point_info'),
    path("about/", about, name='about'),
    path("contact/", contact, name='contact'),
]
