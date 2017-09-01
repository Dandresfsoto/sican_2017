from django.conf.urls import url
from informes.views import InicioView, DeleteInformeView

urlpatterns = [
    url(r'^excel/$', InicioView.as_view()),
    url(r'^excel/eliminar/(?P<pk>[0-9]+)/$', DeleteInformeView.as_view()),
]