from django.conf.urls import url
from bases.views import DepartamentoListView, NuevoDepartamentoView, UpdateDepartamentoView, DeleteDepartamentoView
from bases.views import MunicipioListView, NuevoMunicipioView,UpdateMunicipioView, DeleteMunicipioView
from bases.views import SecretariaListView, NuevoSecretariaView, UpdateSecretariaView, DeleteSecretariaView
from bases.views import RadicadoListView, NuevoRadicadoView, UpdateRadicadoView, DeleteRadicadoView

urlpatterns = [
    url(r'^departamentos/$', DepartamentoListView.as_view()),
    url(r'^departamentos/nuevo/$', NuevoDepartamentoView.as_view()),
    url(r'^departamentos/editar/(?P<pk>[0-9]+)/$', UpdateDepartamentoView.as_view()),
    url(r'^departamentos/eliminar/(?P<pk>[0-9]+)/$', DeleteDepartamentoView.as_view()),

    url(r'^municipios/$', MunicipioListView.as_view()),
    url(r'^municipios/nuevo/$', NuevoMunicipioView.as_view()),
    url(r'^municipios/editar/(?P<pk>[0-9]+)/$', UpdateMunicipioView.as_view()),
    url(r'^municipios/eliminar/(?P<pk>[0-9]+)/$', DeleteMunicipioView.as_view()),

    url(r'^secretarias/$', SecretariaListView.as_view()),
    url(r'^secretarias/nuevo/$', NuevoSecretariaView.as_view()),
    url(r'^secretarias/editar/(?P<pk>[0-9]+)/$', UpdateSecretariaView.as_view()),
    url(r'^secretarias/eliminar/(?P<pk>[0-9]+)/$', DeleteSecretariaView.as_view()),

    url(r'^radicados/$', RadicadoListView.as_view()),
    url(r'^radicados/nuevo/$', NuevoRadicadoView.as_view()),
    url(r'^radicados/editar/(?P<pk>[0-9]+)/$', UpdateRadicadoView.as_view()),
    url(r'^radicados/eliminar/(?P<pk>[0-9]+)/$', DeleteRadicadoView.as_view()),
]