from django.conf.urls import url
from lideres.views import InicioView, VinculosView, LegalizacionView, LegalizacionCompletaView
from formadores.views import NuevaSolicitudTransportesView, SubirSoporteTransportesView, OtroSiView, OtroSiCompletoView
from lideres import views

urlpatterns = [
    #url(r'^$', InicioView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/$', VinculosView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/legalizacion/$', LegalizacionView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/legalizacion/completo/$', LegalizacionCompletaView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/transportes/$', TransportesView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/transportes/nueva/$', NuevaSolicitudTransportesView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/transportes/soporte/(?P<id_soporte>[0-9]+)/$', SubirSoporteTransportesView.as_view()),

    url(r'^legalizacion/$', views.LegalizacionContratosView.as_view()),
    url(r'^legalizacion/contrato/(?P<id_contrato>[0-9]+)/$', views.LegalizacionContratoView.as_view()),
    url(r'^seguridadsocial/$', views.LegalizacionSeguridadView.as_view()),
    url(r'^seguridadsocial/contrato/(?P<id_contrato>[0-9]+)/$', views.SoportesSeguridadSocialView.as_view()),
]