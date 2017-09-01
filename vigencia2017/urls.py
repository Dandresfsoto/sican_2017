from django.conf.urls import url
from vigencia2017 import views

urlpatterns = [
    url(r'^codigosdane/$', views.ListadoCodigosDaneView.as_view()),
    url(r'^codigosdane/nuevo/$', views.NuevoCodigoDaneView.as_view()),
    url(r'^codigosdane/editar/(?P<pk>[0-9]+)/$', views.UpdateCodigoDaneView.as_view()),

    url(r'^grupos/$', views.ListadoGruposFormacionView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/$', views.ListadoGruposFormadorView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/nuevo/$', views.NuevoGrupoFormadorView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/grupo/(?P<id_grupo>[0-9]+)/$', views.ListadoInscritosGrupoView.as_view()),

    url(r'^grupos/formador/(?P<pk>[0-9]+)/conectividad/(?P<id_grupo>[0-9]+)/$', views.ConectividadGrupoView.as_view()),

    url(r'^grupos/formador/(?P<pk>[0-9]+)/evidencias/(?P<id_grupo>[0-9]+)/$', views.ArbolDiplomadoView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/evidencias/(?P<id_grupo>[0-9]+)/id/(?P<id_entregable>[0-9]+)/$', views.ListaEvidenciasEntregableView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/evidencias/(?P<id_grupo>[0-9]+)/id/(?P<id_entregable>[0-9]+)/nuevo/$', views.NuevaEvidenciasEntregableView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/evidencias/(?P<id_grupo>[0-9]+)/id/(?P<id_entregable>[0-9]+)/masivo/$', views.MasivoEvidenciasEntregableView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/evidencias/(?P<id_grupo>[0-9]+)/id/(?P<id_entregable>[0-9]+)/editar/(?P<id_evidencia>[0-9]+)/$', views.EditarEvidenciaEntregableView.as_view()),
    url(r'^grupos/formador/(?P<pk>[0-9]+)/evidencias/(?P<id_grupo>[0-9]+)/id/(?P<id_entregable>[0-9]+)/eliminar/(?P<id_evidencia>[0-9]+)/$', views.DeleteEvidenciaEntregableView.as_view()),


    url(r'^grupos/formador/(?P<pk>[0-9]+)/grupo/(?P<id_grupo>[0-9]+)/nuevo/$', views.NuevoBeneficiarioGrupoView.as_view()),

    url(r'^grupos/formador/(?P<pk>[0-9]+)/grupo/(?P<id_grupo>[0-9]+)/beneficiario/(?P<id_beneficiario>[0-9]+)/$', views.EditarBeneficiarioGrupoView.as_view()),

    url(r'^valor_contratos/$', views.ListadoValorContratosView.as_view()),
    url(r'^valor_contratos/nuevo/$', views.NuevoValorContratoView.as_view()),

    url(r'^valor_contratos/(?P<id_contrato>[0-9]+)/diplomado/(?P<id_diplomado>[0-9]+)/$', views.ValorProductosView.as_view()),

    url(r'^cargar_matriz/$', views.ListadoCargaMatrizView.as_view()),
    url(r'^cargar_matriz/nuevo/$', views.NuevaCargaMatrizView.as_view()),
    url(r'^cargar_matriz/pendientes/(?P<pk>[0-9]+)/$', views.ListadoCambioMatrizView.as_view()),

    url(r'^evidencias/codigos/$', views.EvidenciasListView.as_view()),
    url(r'^evidencias/cedula/$', views.BeneficiarioEvidenciaCedulaList.as_view()),
    url(r'^evidencias/cedula/beneficiario/(?P<id_beneficiario>[0-9]+)/$', views.BeneficiarioEvidenciaCedulaProductoList.as_view()),


    url(r'^reds/$', views.RedsListView.as_view()),
    url(r'^reds/nuevo/$', views.NuevoRedView.as_view()),
]