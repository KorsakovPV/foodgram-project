from django.urls import path, include

from users.views import signup

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
]
