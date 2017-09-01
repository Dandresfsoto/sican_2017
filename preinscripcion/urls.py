from django.conf.urls import url
from preinscripcion.views import ConsultaView, RegistroView, UpdateRegistroView, PreregistroView, DiplomaView, Completo, DiplomaReingresoView
from preinscripcion.views import ConsultaSedBogotaView, RegistroSedBogotaView, UpdateSedBogotaView

urlpatterns = [
    url(r'^$', ConsultaView.as_view()),
    url(r'^registro/(?P<cedula>[0-9]+)/$', RegistroView.as_view()),
    url(r'^registro/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),

    url(r'^modificar/(?P<cedula>[0-9]+)/$', UpdateRegistroView.as_view()),
    url(r'^modificar/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),

    url(r'^preregistro/(?P<cedula>[0-9]+)/$', PreregistroView.as_view()),
    url(r'^preregistro/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),

    url(r'^diploma/(?P<cedula>[0-9]+)/$', DiplomaView.as_view()),
    url(r'^diploma/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),

    url(r'^diploma_reingreso/(?P<cedula>[0-9]+)/$', DiplomaReingresoView.as_view()),
    url(r'^diploma_reingreso/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),

    url(r'^sedbogota/$', ConsultaSedBogotaView.as_view()),
    url(r'^sedbogota/registro/(?P<cedula>[0-9]+)/$', RegistroSedBogotaView.as_view()),
    url(r'^sedbogota/registro/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),
    url(r'^sedbogota/modificar/(?P<cedula>[0-9]+)/$', UpdateSedBogotaView.as_view()),
    url(r'^sedbogota/modificar/(?P<cedula>[0-9]+)/completo/$', Completo.as_view()),
]