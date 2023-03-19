from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import RegisterUserForm, LoginUserForm, UserUpdateForm
from .decorators import user_not_authenticated

from karta.utils import DataMixin, menu


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


@login_required
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Ваш профіль оновлено!')
            return redirect('profile', user_form.username)

        for error in list(form.errors):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name='users/profile.html',
            context={'form': form, 'menu': menu}
        )

    return redirect('index')
