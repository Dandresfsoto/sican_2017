from django.conf.urls import url
from encuestas.views import InicioView, EncuestaView, CompletoView,FinalView, EncuestaFinalView,CompletoFinalView
from encuestas.views import ResultadosPercepcionInicialView
from encuestas.views import RespuestasPercepcionInicialView

urlpatterns = [
    url(r'^percepcioninicial/$', InicioView.as_view()),
    url(r'^percepcioninicial/(?P<pk>\w+)/$', EncuestaView.as_view()),
    url(r'^percepcioninicial/(?P<pk>\w+)/completo/$', CompletoView.as_view()),

    url(r'^resultados/percepcioninicial/$', ResultadosPercepcionInicialView.as_view()),
    url(r'^respuestas/percepcioninicial/$', RespuestasPercepcionInicialView.as_view()),

    url(r'^percepcionfinal/$', FinalView.as_view()),
    url(r'^percepcionfinal/(?P<pk>\w+)/$', EncuestaFinalView.as_view()),
    url(r'^percepcionfinal/(?P<pk>\w+)/completo/$', CompletoFinalView.as_view()),
]