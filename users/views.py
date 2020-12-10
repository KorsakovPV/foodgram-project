from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render

from users.forms import CreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


# def signup(request):
#     context = {}
#     form = CreationForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             # return render(request, reverse('index'))
#             return HttpResponseRedirect(reverse(('index')))
#     context['form'] = form
#     return render(request, 'registration/signup.html', context)




class signup(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'