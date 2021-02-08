from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm
from .models import User


class SignUp(CreateView):
    """Регистрация нового пользователя"""

    form_class = CreationForm
    success_url = reverse_lazy('index_view')
    template_name = 'registration/signup.html'

    def get_form_kwargs(self):
        """Функция передает request в forms.py"""

        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs


# def verify(request, uuid):
#     try:
#         user = User.objects.get(verification_uuid=uuid, is_verified=False)
#     except User.DoesNotExist:
#         raise Http404("User does not exist or is already verified")
#
#     user.is_verified = True
#     user.save()
#
#     return redirect('index_view')
