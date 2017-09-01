from django.conf.urls import url
from rest.views import UserList, UserChatList, UserDetail, UserPermissionList, AdministrativosRh,CargosRh
from rest.views import AdministrativosRhSoportes, AdminUserList, GroupUserList, AdminUserPermissionList, TipoSoporteRh
from rest.views import FormadoresRh, FormadoresRhSoportes
from rest.views import DepartamentosList, MunicipiosList, SecretariasList, RadicadosList
from rest.views import MunicipiosChainedList, RadicadosChainedList
from rest.views import SolicitudesTransporteList, InformesExcelList, ReportesView,PreinscritosList, ResultadosPercepcionInicial
from rest.views import DiplomadosList, NivelesList, SesionesList, SolicitudesTransporteFormacionList, SolicitudesTransporteFormadorList
from rest.views import SolicitudesTransporteFormadorFinancieraList, EntregablesList
from rest.views import FormadoresCronogramasList, FormadoresCronogramasFilterList, SecretariasChainedList
from rest.views import SemanasList, LideresRh, LideresRhSoportes
from rest.views import SemanasFormacionList, FormadoresFinancieraCronogramasList
from rest.views import ResultadosPercepcionInicialList, RadicadosRetomaList, RetomaList
from rest.views import MatricesDiplomadosList, AutocompleteRadicados, GruposChainedList
from rest.views import FormadoresGrupos, FormadoresGruposLista, ContratosValorList, EntregablesValorList, FormadoresRevision
from rest.views import FormadoresRevisionFormador, CortesList, NegociadoresRh
from rest.views import RequerimientosContratacion, AutocompleteMunicipios, RequerimientosContratacionRespuesta
from rest.views import CargaMasivaMatrices, FormadoresListEvidencias, NivelesListEvidencias, SesionesListEvidencias, EntregablesListEvidencias
from rest.views import SoportesListEvidencias,Cedulas2BeneficiariosId
from rest.views import DelegacionRequerimientos, EvidenciasCodigos
from rest.views import RedList, CargaMasivaEvidenciasList, DiplomadosEvidenciasList, FormadoresConsolidadoRh,CertificadosEscuelaTic
from rest.views import RendimientoAuxiliaresList, AcividadesList, BeneficiariosListView, FormadoresContratosFormador
from rest.views import BeneficiariosCedulaListView, BeneficiariosCedulaProductosListView
from rest.views import RedSubsanacionList
from rest.views import EvidenciasSubsanacionCodigos, EvidenciasSubsanacionCodigosSubsanacion, NegociadoresRhSoportes,CodigosDaneList
from rest import views

urlpatterns = [

    #----------------------------------------------- RH ----------------------------------------------------------------
    url(r'rh/personal/administrativos/$', views.AdministrativosRh.as_view()),
    url(r'rh/personal/soportes_administrativos/(?P<id_administrativo>\w+)/$', views.AdministrativosRhSoportes.as_view()),
    url(r'rh/personal/lideres/$', views.LideresRh.as_view()),
    url(r'rh/personal/soportes_lideres/(?P<id_lider>\w+)/$', views.LideresRhSoportes.as_view()),
    url(r'rh/personal/negociadores/$', views.NegociadoresRh.as_view()),
    url(r'rh/personal/soportes_negociadores/(?P<id_negociador>\w+)/$', views.NegociadoresRhSoportes.as_view()),
    url(r'rh/personal/formadores/$', views.FormadoresRh.as_view()),
    url(r'rh/personal/soportes_formadores/(?P<id_formador>\w+)/$', views.FormadoresRhSoportes.as_view()),
    url(r'rh/personal/cargos/$', views.CargosRh.as_view()),
    url(r'rh/personal/tipo_soporte/$', views.TipoSoporteRh.as_view()),
    url(r'rh/contratacion/contratos/formadores/$', views.ContratosFormadoresView.as_view()),
    url(r'rh/contratacion/contratos/formadores/(?P<id_formador>\w+)/$', views.ContratoFormadorView.as_view()),
    url(r'rh/contratacion/solicitud_soportes/formadores/$', views.SolicitudSoportesFormadorView.as_view()),

    url(r'rh/contratacion/contratos/lideres/$', views.ContratosLideresView.as_view()),
    url(r'rh/contratacion/contratos/lideres/(?P<id_lider>\w+)/$', views.ContratoLiderView.as_view()),
    url(r'rh/contratacion/solicitud_soportes/lideres/$', views.SolicitudSoportesLiderView.as_view()),

    url(r'rh/contratacion/contratos/negociadores/$', views.ContratosNegociadoresView.as_view()),
    url(r'rh/contratacion/contratos/negociadores/(?P<id_negociador>\w+)/$', views.ContratoNegociadorView.as_view()),
    url(r'rh/contratacion/solicitud_soportes/negociadores/$', views.SolicitudSoportesNegociadorView.as_view()),
    #--------------------------------------------- CONTRATOS -----------------------------------------------------------

    url(r'contratos/legalizacion/administrativos/$', views.ContratoAdministrativosUserView.as_view()),
    url(r'contratos/legalizacion/formadores/$', views.ContratoFormadorUserView.as_view()),
    url(r'contratos/legalizacion/lideres/$', views.ContratoLiderUserView.as_view()),
    url(r'contratos/legalizacion/negociadores/$', views.ContratoNegociadorUserView.as_view()),
    url(r'contratos/informacion/formadores/$', views.ContratoInfoView.as_view()),

    #-------------------------------------------------------------------------------------------------------------------


    #-------------------------------------------------- REST -----------------------------------------------------------

    url(r'usuarios/permisos/$', UserPermissionList.as_view()),
    url(r'vigencia_2017/codigos_dane/$', CodigosDaneList.as_view()),
    url(r'vigencia_2017/grupos/$', views.Vigencia2017GruposList.as_view()),
    url(r'vigencia_2017/grupos/formador/(?P<id_contrato>\w+)/$', views.Vigencia2017ContratoList.as_view()),
    url(r'vigencia_2017/grupos/formador/(?P<id_contrato>\w+)/grupo/(?P<id_grupo>\w+)/$', views.Vigencia2017BeneficiariosList.as_view()),

    url(r'vigencia_2017/grupos/formador/(?P<id_contrato>\w+)/evidencias/(?P<id_grupo>\w+)/$', views.Vigencia2017TreeDiplomado.as_view()),
    url(r'vigencia_2017/grupos/formador/(?P<id_contrato>\w+)/evidencias/(?P<id_grupo>\w+)/id/(?P<id_entregable>\w+)/$', views.ListaSoportesVigencia2017.as_view()),

    url(r'vigencia_2017/valor_contratos/$', views.ValorContratosList.as_view()),
    url(r'vigencia_2017/cargar_matriz/$', views.CargaMatrizList.as_view()),
    url(r'vigencia_2017/cargar_matriz/pendientes/(?P<id_masivo>\w+)/$', views.PendientesMatrizList.as_view()),
    url(r'vigencia_2017/cedulas/id/',views.Cedulas2BeneficiariosIdVigencia2017.as_view()),
    url(r'vigencia_2017/cedulas/id_grupo/(?P<id_grupo>\w+)/',views.GrupoCedulas2BeneficiariosIdVigencia2017.as_view()),

    url(r'vigencia_2017/evidencias/codigos/',views.EvidenciasCodigosVigencia2017.as_view()),
    url(r'vigencia_2017/evidencias/cedula/$', views.BeneficiariosVigencia2017CedulaListView.as_view()),
    url(r'vigencia_2017/evidencias/cedula/(?P<id_beneficiario>\w+)/$', views.BeneficiariosCedulaProductosVigencia2017ListView.as_view()),
    url(r'vigencia_2017/reds/lista/',views.RedListVigencia2017.as_view()),
    #-------------------------------------------------------------------------------------------------------------------

    #--------------------------------------------- BENEFICIARIOS -------------------------------------------------------
    url(r'beneficiarios/grupos/$', views.BeneficiariosGruposList.as_view()),
    url(r'beneficiarios/(?P<id_grupo>\w+)/$', views.BeneficiariosGroupList.as_view()),
    #-------------------------------------------------------------------------------------------------------------------


    url(r'usuarios/chat_list/$', UserList.as_view()),
    url(r'usuarios/chat_list/(?P<id>\w+)/$', UserDetail.as_view()),
    url(r'usuarios/chat_last/$', UserChatList.as_view()),





    url(r'adminuser/usuarios/$', AdminUserList.as_view()),
    url(r'adminuser/grupos/$', GroupUserList.as_view()),



    url(r'adminuser/permisos/$', AdminUserPermissionList.as_view()),



    url(r'bases/departamentos/$', DepartamentosList.as_view()),
    url(r'bases/municipios/$', MunicipiosList.as_view()),
    url(r'bases/secretarias/$', SecretariasList.as_view()),
    url(r'bases/radicados/$', RadicadosList.as_view()),
    url(r'chained/municipios/$', MunicipiosChainedList.as_view()),
    url(r'chained/radicados/$', RadicadosChainedList.as_view()),
    url(r'chained/secretarias/$', SecretariasChainedList.as_view()),
    url(r'chained/grupos/$', GruposChainedList.as_view()),

    url(r'financiera/transportes/$', SolicitudesTransporteList.as_view()),
    url(r'financiera/transportes/(?P<id_formador>\w+)/$', SolicitudesTransporteFormadorFinancieraList.as_view()),


    url(r'informes/excel/$', InformesExcelList.as_view()),
    url(r'reportes/$', ReportesView.as_view()),
    url(r'formacion/preinscritos/$', PreinscritosList.as_view()),

    url(r'encuestas/percepcioninicial/$', ResultadosPercepcionInicial.as_view()),
    url(r'encuestas/percepcioninicialresultados/$', ResultadosPercepcionInicialList.as_view()),


    url(r'financiera/diplomados/$', DiplomadosList.as_view()),
    url(r'financiera/niveles/$', NivelesList.as_view()),
    url(r'financiera/sesiones/$', SesionesList.as_view()),
    url(r'financiera/entregables/$', EntregablesList.as_view()),

    url(r'formacion/transportes/$', SolicitudesTransporteFormacionList.as_view()),
    url(r'formacion/transportes/(?P<id_formador>\w+)/$', SolicitudesTransporteFormadorList.as_view()),

    url(r'formacion/cronogramas/(?P<id_semana>\w+)/$', FormadoresCronogramasList.as_view()),
    url(r'formacion/cronogramas/(?P<id_formador>\w+)/(?P<id_semana>\w+)/$', FormadoresCronogramasFilterList.as_view()),

    url(r'financiera/cronogramas/$', SemanasList.as_view()),
    url(r'financiera/cronogramas/(?P<id_semana>\w+)/$', FormadoresFinancieraCronogramasList.as_view()),

    url(r'formacion/semanas/$', SemanasFormacionList.as_view()),
    url(r'acceso/radicadosretoma/$', RadicadosRetomaList.as_view()),

    url(r'acceso/retoma/$', RetomaList.as_view()),

    url(r'matrices/diplomados/(?P<diplomado>\w+)/$', MatricesDiplomadosList.as_view()),




    url(r'autocomplete/radicados/$', AutocompleteRadicados.as_view()),
    url(r'autocomplete/municipios/$', AutocompleteMunicipios.as_view()),


    url(r'formacion/grupos/$', FormadoresGrupos.as_view()),
    url(r'formacion/grupos/(?P<id_formador>\w+)/$', FormadoresGruposLista.as_view()),

    url(r'financiera/contratos/$', ContratosValorList.as_view()),
    url(r'financiera/entregablesvalor/(?P<id_contrato>\w+)/$', EntregablesValorList.as_view()),

    url(r'formadores/revision/$', FormadoresRevision.as_view()),
    url(r'formadores/revision/(?P<id_formador>\w+)/(?P<id_cargo>\w+)/$', FormadoresRevisionFormador.as_view()),
    url(r'formadores/contratos/(?P<id_formador>\w+)/$', FormadoresContratosFormador.as_view()),

    url(r'financiera/cortes/$', CortesList.as_view()),

    url(r'formacion/requerimientoscontratacion/$', RequerimientosContratacion.as_view()),
    url(r'formacion/requerimientoscontratacionrespuesta/$', RequerimientosContratacionRespuesta.as_view()),

    url(r'cargamasiva/matrices/$', CargaMasivaMatrices.as_view()),

    url(r'evidencias/diplomados/$', DiplomadosEvidenciasList.as_view()),
    url(r'evidencias/formadores/(?P<id_diplomado>\w+)/$', FormadoresListEvidencias.as_view()),
    url(r'evidencias/niveles/(?P<id_diplomado>\w+)/$', NivelesListEvidencias.as_view()),
    url(r'evidencias/sesiones/(?P<id_nivel>\w+)/$', SesionesListEvidencias.as_view()),
    url(r'evidencias/entregables/(?P<id_sesion>\w+)/$', EntregablesListEvidencias.as_view()),
    url(r'evidencias/soportes/(?P<id_entregable>\w+)/(?P<id_formador>\w+)/$', SoportesListEvidencias.as_view()),
    url(r'cedulas/id/',Cedulas2BeneficiariosId.as_view()),

    url(r'requerimientos/delegacion/$', DelegacionRequerimientos.as_view()),

    url(r'evidencias/codigos/',EvidenciasCodigos.as_view()),


    url(r'reds/lista/',RedList.as_view()),

    url(r'cargamasivaevidencias/lista/',CargaMasivaEvidenciasList.as_view()),

    url(r'rh/consolidadoformadores/',FormadoresConsolidadoRh.as_view()),

    url(r'diplomas/escuelatic/',CertificadosEscuelaTic.as_view()),

    url(r'auxiliares/rendimiento/',RendimientoAuxiliaresList.as_view()),

    url(r'evidencias/actividades/(?P<id_diplomado>\w+)/$', AcividadesList.as_view()),

    url(r'evidencias/beneficiarios/(?P<id_actividad>\w+)/$', BeneficiariosListView.as_view()),

    url(r'evidencias/cedula/$', BeneficiariosCedulaListView.as_view()),

    url(r'evidencias/cedula/(?P<id_beneficiario>\w+)/$', BeneficiariosCedulaProductosListView.as_view()),

    url(r'reds/subsanacion/',RedSubsanacionList.as_view()),

    url(r'reds/subsanacionevidencias/red/(?P<id_red>\w+)/',EvidenciasSubsanacionCodigos.as_view()),

    url(r'reds/subsanacionevidencias_id/red/(?P<id_red>\w+)/evidencia/(?P<id_evidencia>\w+)/',EvidenciasSubsanacionCodigosSubsanacion.as_view()),

    url(r'cedula/(?P<cedula>\d+)/',views.CedulaDocente.as_view()),

    url(r'rh/contratos/formadores/cohortes/',views.CohortesFormadorList.as_view()),

    url(r'ples/',views.BeneficiariosPleList.as_view()),
]