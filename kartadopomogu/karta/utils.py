from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [{'title': 'Головна Сторінка', 'url_name': 'index'},
        {'title': 'Створити Допомогу', 'url_name': 'add_point'},
        {'title': 'Ваші Допомогу', 'url_name': 'users_points'},
        {'title': 'Відгук', 'url_name': 'contact'},
        {'title': 'Про нас', 'url_name': 'about'},
        ]


def get_user_context(user, context):
    user_menu = menu.copy()
    if not user.is_authenticated:
        user_menu.pop(1)
        user_menu.pop(1)
    context['menu'] = user_menu
    return context


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            user_menu.pop(1)
        context['menu'] = user_menu
        return context

