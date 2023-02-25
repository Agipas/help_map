from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path("", PointPage.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
