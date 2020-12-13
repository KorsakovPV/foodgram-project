from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    #TODO Валидация пароля, желательно после регистрации быть залогиненым.
    form_class = CreationForm
    success_url = reverse_lazy('login')#('login')('index')
    # success_url = '/auth/login/'
    template_name = 'registration/signup.html'
