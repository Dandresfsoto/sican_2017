from django.conf.urls import url
from formadores.views import InicioView, VinculosView, LegalizacionView, LegalizacionCompletaView, TransportesView
from formadores.views import NuevaSolicitudTransportesView, SubirSoporteTransportesView, OtroSiView, OtroSiCompletoView
from formadores.views import EntregablesView, SeguridadSocialView, SeguridadSocialCompletaView,PagosView, PagosCorteView, PagosCorteEntregableView
from formadores.views import TipologiasView, TipologiasPagosView
from formadores import views

urlpatterns = [
    #url(r'^$', InicioView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/$', VinculosView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/otrosi/$', OtroSiView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/otrosi/completo/$', OtroSiCompletoView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/legalizacion/$', LegalizacionView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/legalizacion/completo/$', LegalizacionCompletaView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/transportes/$', TransportesView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/transportes/nueva/$', NuevaSolicitudTransportesView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/transportes/soporte/(?P<id_soporte>[0-9]+)/$', SubirSoporteTransportesView.as_view()),

    #url(r'^(?P<cedula>[0-9]+)/entregables/$', TipologiasView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/entregables/cargo/(?P<id_cargo>[0-9]+)/$', EntregablesView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/seguridadsocial/$', SeguridadSocialView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/seguridadsocial/completo/$', SeguridadSocialCompletaView.as_view()),

    #url(r'^(?P<cedula>[0-9]+)/pagos/$', TipologiasPagosView.as_view()),
    #url(r'^(?P<cedula>[0-9]+)/pagos/cargo/(?P<id_cargo>[0-9]+)/$', PagosView.as_view()),

    #url(r'^(?P<cedula>[0-9]+)/pagos/cargo/(?P<id_cargo>[0-9]+)/(?P<id_corte>[0-9]+)/$', PagosCorteView.as_view()),

    #url(r'^(?P<cedula>[0-9]+)/pagos/cargo/(?P<id_cargo>[0-9]+)/(?P<id_corte>[0-9]+)/(?P<id_pago>[0-9]+)/$', PagosCorteEntregableView.as_view()),
    url(r'^legalizacion/$', views.LegalizacionContratosView.as_view()),
    url(r'^legalizacion/contrato/(?P<id_contrato>[0-9]+)/$', views.LegalizacionContratoView.as_view()),
    url(r'^seguridadsocial/$', views.LegalizacionSeguridadView.as_view()),
    url(r'^seguridadsocial/contrato/(?P<id_contrato>[0-9]+)/$', views.SoportesSeguridadSocialView.as_view()),
]