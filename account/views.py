from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print("User:", user)
        if user:
            print("Is superuser:", user.is_superuser)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect(reverse('car'))
            else:
                return redirect(reverse('index'))
        else:
            return render(request, self.template_name, {'error': 'Неверные учетные данные'})


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser, login_url='login')
def admin_action(request):
    return render(request, 'add_car.html')
