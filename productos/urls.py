from django.conf.urls import url
from productos.views import DiplomadosListView, DiplomadoCreateView,DiplomadoUpdateView
from productos.views import NivelesListView, NivelesCreateView, NivelesUpdateView
from productos.views import SesionesListView, SesionesCreateView, SesionesUpdateView
from productos.views import EntregablesListView, EntregablesCreateView, EntregablesUpdateView

urlpatterns = [
    url(r'^diplomados/$', DiplomadosListView.as_view()),
    url(r'^diplomados/nuevo/$', DiplomadoCreateView.as_view()),
    url(r'^diplomados/editar/(?P<pk>\w+)/$', DiplomadoUpdateView.as_view()),

    url(r'^niveles/$', NivelesListView.as_view()),
    url(r'^niveles/nuevo/$', NivelesCreateView.as_view()),
    url(r'^niveles/editar/(?P<pk>\w+)/$', NivelesUpdateView.as_view()),

    url(r'^sesiones/$', SesionesListView.as_view()),
    url(r'^sesiones/nuevo/$', SesionesCreateView.as_view()),
    url(r'^sesiones/editar/(?P<pk>\w+)/$', SesionesUpdateView.as_view()),

    url(r'^entregables/$', EntregablesListView.as_view()),
    url(r'^entregables/nuevo/$', EntregablesCreateView.as_view()),
    url(r'^entregables/editar/(?P<pk>\w+)/$', EntregablesUpdateView.as_view()),
]