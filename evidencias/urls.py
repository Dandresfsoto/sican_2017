from django.conf.urls import url
from evidencias.views import DiplomadosListView, FormadoresListView, NivelesListView, SesionesListView, EntregablesListView, SoportesListView
from evidencias.views import NuevoSoporteView, UpdateSoporteView, DeleteSoporteView, EvidenciasListView
from evidencias.views import RedsListView, NuevoRedView
from evidencias.views import CargaMasivaListView, NuevoCargaMasivaView, UpdateRedView
from evidencias.views import AuxiliaresListView, DiplomadosActividadesListView, ActividadesListView
from evidencias.views import BeneficiariosEvidenciaListView
from evidencias.views import BeneficiarioEvidenciaCedulaList, BeneficiarioEvidenciaCedulaProductoList
from evidencias.views import SubsanacionListView
from evidencias.views import SubsanacionEvidenciasListView, SubsanacionEvidenciasFormView
from evidencias.views import SubsanacionEvidenciasBeneficiarioView, ListaSubsanacionEvidenciaView, PleListView, PleBeneficiarioView

urlpatterns = [
    url(r'^general/$', DiplomadosListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/$', FormadoresListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/$', NivelesListView.as_view()),

    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/$', SesionesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/$', EntregablesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/$', SoportesListView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/nuevo/$', NuevoSoporteView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', UpdateSoporteView.as_view()),
    url(r'^general/diplomado/(?P<id_diplomado>[0-9]+)/formador/(?P<id_formador>[0-9]+)/nivel/(?P<id_nivel>[0-9]+)/sesion/(?P<id_sesion>[0-9]+)/entregable/(?P<id_entregable>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', DeleteSoporteView.as_view()),

    url(r'^codigos/$', EvidenciasListView.as_view()),

    url(r'^reds/$', RedsListView.as_view()),
    url(r'^reds/nuevo/$', NuevoRedView.as_view()),
    url(r'^reds/editar/(?P<pk>[0-9]+)/$', UpdateRedView.as_view()),

    url(r'^cargamasiva/$', CargaMasivaListView.as_view()),
    url(r'^cargamasiva/nuevo/$', NuevoCargaMasivaView.as_view()),

    url(r'^rendimiento/$', AuxiliaresListView.as_view()),

    url(r'^actividades/$', DiplomadosActividadesListView.as_view()),
    url(r'^actividades/diplomado/(?P<id_diplomado>[0-9]+)/$', ActividadesListView.as_view()),

    url(r'^actividades/diplomado/(?P<id_diplomado>[0-9]+)/evidencia/(?P<id_evidencia>[0-9]+)/$', BeneficiariosEvidenciaListView.as_view()),

    url(r'^cedula/$', BeneficiarioEvidenciaCedulaList.as_view()),

    url(r'^cedula/beneficiario/(?P<id_beneficiario>[0-9]+)/$', BeneficiarioEvidenciaCedulaProductoList.as_view()),

    url(r'^subsanacion/$', SubsanacionListView.as_view()),

    url(r'^subsanacion/red/(?P<id_red>[0-9]+)/$', SubsanacionEvidenciasListView.as_view()),

    url(r'^subsanacion/red/(?P<id_red>[0-9]+)/evidencia/(?P<id_evidencia>[0-9]+)/$', ListaSubsanacionEvidenciaView.as_view()),

    url(r'^subsanacion/red/(?P<id_red>[0-9]+)/evidencia/(?P<id_evidencia>[0-9]+)/nuevo/$', SubsanacionEvidenciasFormView.as_view()),

    url(r'^subsanacion/red/(?P<id_red>[0-9]+)/evidencia/(?P<id_evidencia>[0-9]+)/nuevo/beneficiario/(?P<id_beneficiario>[0-9]+)/$', SubsanacionEvidenciasBeneficiarioView.as_view()),

    url(r'^ple/$', PleListView.as_view()),

    url(r'^ple/editar/(?P<id_beneficiario>[0-9]+)/$', PleBeneficiarioView.as_view()),
]