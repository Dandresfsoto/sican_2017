from django.conf.urls import url
from rh.views import ListaRequerimientosContratacionView, NuevoRequerimientoContratacionView, FormadoresConsolidadoView
from rh import views

urlpatterns = [

    url(r'^personal/$', views.PersonalView.as_view()),

    url(r'^personal/administrativos/$', views.AdministrativoView.as_view()),
    url(r'^personal/administrativos/nuevo/$', views.NuevoAdministrativoView.as_view()),
    url(r'^personal/administrativos/editar/(?P<pk>[0-9]+)/$', views.UpdateAdministrativoView.as_view()),
    url(r'^personal/administrativos/eliminar/(?P<pk>[0-9]+)/$', views.DeleteAdministrativoView.as_view()),

    url(r'^personal/administrativos/soportes/(?P<pk>[0-9]+)/$', views.SoporteAdministrativoView.as_view()),
    url(r'^personal/administrativos/soportes/(?P<pk>[0-9]+)/nuevo/$', views.NuevoSoporteAdministrativoView.as_view()),
    url(r'^personal/administrativos/soportes/(?P<pk>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', views.UpdateSoporteAdministrativoView.as_view()),
    url(r'^personal/administrativos/soportes/(?P<pk>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', views.DeleteSoporteAdministrativoView.as_view()),

    url(r'^personal/acceso/$', views.AccesoView.as_view()),
    url(r'^personal/acceso/lideres/$', views.LideresView.as_view()),
    url(r'^personal/acceso/lideres/nuevo/$', views.NuevoLiderView.as_view()),
    url(r'^personal/acceso/lideres/editar/(?P<pk>[0-9]+)/$', views.UpdateLiderView.as_view()),
    url(r'^personal/acceso/lideres/eliminar/(?P<pk>[0-9]+)/$', views.DeleteLiderView.as_view()),

    url(r'^personal/acceso/lideres/soportes/(?P<pk>[0-9]+)/$', views.SoporteLiderView.as_view()),
    url(r'^personal/acceso/lideres/soportes/(?P<pk>[0-9]+)/nuevo/$', views.NuevoSoporteLiderView.as_view()),
    url(r'^personal/acceso/lideres/soportes/(?P<pk>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', views.UpdateSoporteLiderView.as_view()),
    url(r'^personal/acceso/lideres/soportes/(?P<pk>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', views.DeleteSoporteLiderView.as_view()),

    url(r'^personal/acceso/negociadores/$', views.NegociadoresView.as_view()),
    url(r'^personal/acceso/negociadores/nuevo/$', views.NuevoNegociadorView.as_view()),
    url(r'^personal/acceso/negociadores/editar/(?P<pk>[0-9]+)/$', views.UpdateNegociadorView.as_view()),
    url(r'^personal/acceso/negociadores/eliminar/(?P<pk>[0-9]+)/$', views.DeleteNegociadorView.as_view()),

    url(r'^personal/acceso/negociadores/soportes/(?P<pk>[0-9]+)/$', views.SoporteNegociadorView.as_view()),
    url(r'^personal/acceso/negociadores/soportes/(?P<pk>[0-9]+)/nuevo/$', views.NuevoSoporteNegociadorView.as_view()),
    url(r'^personal/acceso/negociadores/soportes/(?P<pk>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', views.UpdateSoporteNegociadorView.as_view()),
    url(r'^personal/acceso/negociadores/soportes/(?P<pk>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', views.DeleteSoporteNegociadorView.as_view()),

    url(r'^personal/formadores/$', views.FormadoresView.as_view()),
    url(r'^personal/formadores/nuevo/$', views.NuevoFormadorView.as_view()),
    url(r'^personal/formadores/editar/(?P<pk>[0-9]+)/$', views.UpdateFormadorView.as_view()),
    url(r'^personal/formadores/eliminar/(?P<pk>[0-9]+)/$', views.DeleteFormadorView.as_view()),

    url(r'^personal/formadores/soportes/(?P<pk>[0-9]+)/$', views.SoporteFormadorView.as_view()),
    url(r'^personal/formadores/soportes/(?P<pk>[0-9]+)/nuevo/$', views.NuevoSoporteFormadorView.as_view()),
    url(r'^personal/formadores/soportes/(?P<pk>[0-9]+)/editar/(?P<id_soporte>[0-9]+)/$', views.UpdateSoporteFormadorView.as_view()),
    url(r'^personal/formadores/soportes/(?P<pk>[0-9]+)/eliminar/(?P<id_soporte>[0-9]+)/$', views.DeleteSoporteFormadorView.as_view()),

    url(r'^personal/cargos/$', views.CargosView.as_view()),
    url(r'^personal/cargos/nuevo/$', views.NuevoCargoView.as_view()),
    url(r'^personal/cargos/editar/(?P<pk>[0-9]+)/$', views.UpdateCargoView.as_view()),
    url(r'^personal/cargos/eliminar/(?P<pk>[0-9]+)/$', views.DeleteCargoView.as_view()),

    url(r'^personal/tipo_soporte/$', views.TipoSoporteAdministrativoView.as_view()),
    url(r'^personal/tipo_soporte/nuevo/$', views.NuevoTipoSoporteAdministrativoView.as_view()),
    url(r'^personal/tipo_soporte/editar/(?P<pk>[0-9]+)/$', views.UpdateTipoSoporteAdministrativoView.as_view()),
    url(r'^personal/tipo_soporte/eliminar/(?P<pk>[0-9]+)/$', views.DeleteTipoSoporteAdministrativoView.as_view()),

    url(r'^contratacion/$', views.ContratacionView.as_view()),





    url(r'^contratacion/contratos/formadores/$', views.ContratosFormadoresGeneralView.as_view()),
    url(r'^contratacion/contratos/formadores/lista/$', views.ContratosFormadoresView.as_view()),
    url(r'^contratacion/contratos/formadores/lista/editar/(?P<id_formador>[0-9]+)/$', views.ContratoFormadorView.as_view()),
    url(r'^contratacion/contratos/formadores/lista/editar/(?P<id_formador>[0-9]+)/nuevo/$', views.NuevoContratoFormadorView.as_view()),
    url(r'^contratacion/contratos/formadores/lista/editar/(?P<id_formador>[0-9]+)/editar/(?P<id_contrato>[0-9]+)/$', views.UpdateContratoFormadorView.as_view()),

    url(r'^contratacion/contratos/formadores/cohortes/$', views.CohortesFormadoresView.as_view()),
    url(r'^contratacion/contratos/formadores/cohortes/nuevo/$', views.CohortesFormadoresNuevoView.as_view()),



    url(r'^contratacion/solicitud_soportes/formadores/$', views.SolicitudSoportesFormadoresView.as_view()),
    url(r'^contratacion/solicitud_soportes/formadores/nuevo/$', views.NuevaSolicitudSoportesFormadorView.as_view()),
    url(r'^contratacion/solicitud_soportes/formadores/editar/(?P<id_solicitud_soporte>[0-9]+)/$', views.UpdateSolicitudSoportesFormadorView.as_view()),

    url(r'^contratacion/contratos/lideres/$', views.ContratosLideresView.as_view()),
    url(r'^contratacion/contratos/lideres/editar/(?P<id_lider>[0-9]+)/$', views.ContratoLiderView.as_view()),
    url(r'^contratacion/contratos/lideres/editar/(?P<id_lider>[0-9]+)/nuevo/$', views.NuevoContratoLiderView.as_view()),
    url(r'^contratacion/contratos/lideres/editar/(?P<id_lider>[0-9]+)/editar/(?P<id_contrato>[0-9]+)/$', views.UpdateContratoLiderView.as_view()),

    url(r'^contratacion/solicitud_soportes/lideres/$', views.SolicitudSoportesLideresView.as_view()),
    url(r'^contratacion/solicitud_soportes/lideres/nuevo/$', views.NuevaSolicitudSoportesLiderView.as_view()),
    url(r'^contratacion/solicitud_soportes/lideres/editar/(?P<id_solicitud_soporte>[0-9]+)/$', views.UpdateSolicitudSoportesLiderView.as_view()),

    url(r'^contratacion/contratos/negociadores/$', views.ContratosNegociadoresView.as_view()),
    url(r'^contratacion/contratos/negociadores/editar/(?P<id_negociador>[0-9]+)/$', views.ContratoNegociadorView.as_view()),
    url(r'^contratacion/contratos/negociadores/editar/(?P<id_negociador>[0-9]+)/nuevo/$', views.NuevoContratoNegociadorView.as_view()),
    url(r'^contratacion/contratos/negociadores/editar/(?P<id_negociador>[0-9]+)/editar/(?P<id_contrato>[0-9]+)/$', views.UpdateContratoNegociadorView.as_view()),

    url(r'^contratacion/solicitud_soportes/negociadores/$', views.SolicitudSoportesNegociadoresView.as_view()),
    url(r'^contratacion/solicitud_soportes/negociadores/nuevo/$', views.NuevaSolicitudSoportesNegociadorView.as_view()),
    url(r'^contratacion/solicitud_soportes/negociadores/editar/(?P<id_solicitud_soporte>[0-9]+)/$', views.UpdateSolicitudSoportesNegociadorView.as_view()),

    url(r'^requerimientoscontratacion/$', ListaRequerimientosContratacionView.as_view()),
    url(r'^requerimientoscontratacion/(?P<pk>[0-9]+)/$', NuevoRequerimientoContratacionView.as_view()),
    url(r'^consolidadoformadores/$', FormadoresConsolidadoView.as_view()),
]