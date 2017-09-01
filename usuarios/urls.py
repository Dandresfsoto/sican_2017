from django.conf.urls import url
from usuarios.views import Perfil, ChangePassword

urlpatterns = [
    url(r'^$', Perfil.as_view()),
    url(r'^password/$', ChangePassword.as_view()),
]