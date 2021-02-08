from django.conf.urls import url
from django.urls import include, path

from users.views import SignUp#, verify

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
    #path('verify/(<uuid:uuid>/', verify, name='verify'),
]
