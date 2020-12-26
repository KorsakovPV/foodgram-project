from django.urls import include, path

from .views import SignUp

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
]
