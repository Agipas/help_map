from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import RegisterUserForm, LoginUserForm
from .decorators import user_not_authenticated

from karta.utils import DataMixin


# Create your views here.
@method_decorator(user_not_authenticated, name='dispatch')
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


@method_decorator(user_not_authenticated, name='dispatch')
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Увійти')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('index')


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')
