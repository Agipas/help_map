from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path("add/", addNoteView, name='add_note'),
    path("", PointPage.as_view(), name='index'),
    path('category/<slug:cat_slug>', PointCategory.as_view(), name='category'),
    path("users-points/", UsersPointPage.as_view(), name='users_points'),
    path("new-point/", CreatePoint.as_view(), name='add_point'),
    path("point-info/<slug:point_slug>", ShowPoint.as_view(), name='point_info'),
    path("point/<slug:point_slug>-update", UpdatePoint.as_view(), name='point_update'),
    path("point/<slug:point_slug>-delete", delete_point, name='point_delete'),
    path("about/", about, name='about'),
    path("contact/", contact, name='contact'),
    # path('map/', location_map, name='location_map'),
]
