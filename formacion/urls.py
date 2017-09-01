from django.conf.urls import url
from formacion.views import ListaPreinscritosView, NuevoPreinscritoView, UpdatePreinscritoView,DeletePreinscritoView
from formacion.views import ListaRevisionView
from formacion.views import ListaTransportesView, ListaTransportesAprobadasFinancieraView, ListaTransportesRechazadasView, ListaTransportesPendientesView
from formacion.views import TransporteFormView, TransporteFormUpdateView
from formacion.views import ListaTransportesConsignadasView, ListaTransportesAprobadasLideresView
from formacion.views import ListaCronogramasView, CronogramaFormadorView, CronogramaFormadorNuevoView, CronogramaFormadorUpdateView
from formacion.views import CronogramaFormadorDeleteView, ListaCronogramasSemanaView
from formacion.views import ListadoFormadoresGruposView, FormadoresGruposLista, NuevoGrupoFormador, EditarGrupoFormador, EliminarGrupoFormador
from formacion.views import ListaRevisionFormadorView,NuevaRevisionFormadorView, EditarRevisionFormadorView
from formacion.views import ListaRequerimientosContratacionView, NuevoRequerimientoContratacionView, UpdateRequerimientoContratacionView
from formacion.views import DiplomasEscuelaTic
from formacion.views import ListaRevisionTipologiaView

urlpatterns = [
    url(r'^preinscritos/$', ListaPreinscritosView.as_view()),
    url(r'^preinscritos/nuevo/$', NuevoPreinscritoView.as_view()),
    url(r'^preinscritos/editar/(?P<pk>[0-9]+)/$', UpdatePreinscritoView.as_view()),
    url(r'^preinscritos/eliminar/(?P<pk>[0-9]+)/$', DeletePreinscritoView.as_view()),

    url(r'^transportes/$', ListaTransportesView.as_view()),

    url(r'^transportes/consignadas/(?P<id>[0-9]+)/$', ListaTransportesConsignadasView.as_view()),
    url(r'^transportes/aprobadasfinanciera/(?P<id>[0-9]+)/$', ListaTransportesAprobadasFinancieraView.as_view()),
    url(r'^transportes/aprobadaslideres/(?P<id>[0-9]+)/$', ListaTransportesAprobadasLideresView.as_view()),
    url(r'^transportes/rechazadas/(?P<id>[0-9]+)/$', ListaTransportesRechazadasView.as_view()),

    url(r'^transportes/pendientes/(?P<id>[0-9]+)/$', ListaTransportesPendientesView.as_view()),
    url(r'^transportes/pendientes/(?P<id>[0-9]+)/estado/(?P<id_solicitud>[0-9]+)/$', TransporteFormView.as_view()),
    url(r'^transportes/pendientes/(?P<id>[0-9]+)/editar/(?P<id_solicitud>[0-9]+)/$', TransporteFormUpdateView.as_view()),

    url(r'^cronograma/$', ListaCronogramasView.as_view()),
    url(r'^cronograma/semana/(?P<semana_id>[0-9]+)/$', ListaCronogramasSemanaView.as_view()),
    url(r'^cronograma/semana/(?P<semana_id>[0-9]+)/editar/(?P<id>[0-9]+)/$', CronogramaFormadorView.as_view()),
    url(r'^cronograma/semana/(?P<semana_id>[0-9]+)/editar/(?P<id>[0-9]+)/nuevo/$', CronogramaFormadorNuevoView.as_view()),
    url(r'^cronograma/semana/(?P<semana_id>[0-9]+)/editar/(?P<id>[0-9]+)/entrada/(?P<id_entrada>[0-9]+)/$', CronogramaFormadorUpdateView.as_view()),
    url(r'^cronograma/semana/(?P<semana_id>[0-9]+)/editar/(?P<id>[0-9]+)/eliminar/(?P<id_entrada>[0-9]+)/$', CronogramaFormadorDeleteView.as_view()),

    url(r'^grupos/$', ListadoFormadoresGruposView.as_view()),
    url(r'^grupos/formador/(?P<id_formador>\w+)/$', FormadoresGruposLista.as_view()),
    url(r'^grupos/formador/(?P<id_formador>\w+)/nuevo$', NuevoGrupoFormador.as_view()),
    url(r'^grupos/formador/(?P<id_formador>\w+)/editar/(?P<id_grupo>\w+)/', EditarGrupoFormador.as_view()),
    url(r'^grupos/formador/(?P<id_formador>\w+)/eliminar/(?P<id_grupo>\w+)/', EliminarGrupoFormador.as_view()),

    url(r'^revision/$', ListaRevisionView.as_view()),
    url(r'^revision/(?P<id_formador>\w+)/$', ListaRevisionTipologiaView.as_view()),

    url(r'^revision/(?P<id_formador>\w+)/cargo/(?P<id_cargo>\w+)/$', ListaRevisionFormadorView.as_view()),

    url(r'^revision/(?P<id_formador>\w+)/cargo/(?P<id_cargo>\w+)/nuevo/$', NuevaRevisionFormadorView.as_view()),
    url(r'^revision/(?P<id_formador>\w+)/cargo/(?P<id_cargo>\w+)/editar/(?P<id_revision>\w+)/$', EditarRevisionFormadorView.as_view()),

    url(r'^requerimientoscontratacion/$', ListaRequerimientosContratacionView.as_view()),
    url(r'^requerimientoscontratacion/nuevo/$', NuevoRequerimientoContratacionView.as_view()),
    url(r'^requerimientoscontratacion/(?P<pk>[0-9]+)/$', UpdateRequerimientoContratacionView.as_view()),

    url(r'^diplomas/escuelatic/$', DiplomasEscuelaTic.as_view()),
]