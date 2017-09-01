from django.conf.urls import url
from lideres.views import InicioView, VinculosView, LegalizacionView, LegalizacionCompletaView
from formadores.views import NuevaSolicitudTransportesView, SubirSoporteTransportesView, OtroSiView, OtroSiCompletoView
from negociadores import views

urlpatterns = [
    url(r'^legalizacion/$', views.LegalizacionContratosView.as_view()),
    url(r'^legalizacion/contrato/(?P<id_contrato>[0-9]+)/$', views.LegalizacionContratoView.as_view()),
    url(r'^seguridadsocial/$', views.LegalizacionSeguridadView.as_view()),
    url(r'^seguridadsocial/contrato/(?P<id_contrato>[0-9]+)/$', views.SoportesSeguridadSocialView.as_view()),
]