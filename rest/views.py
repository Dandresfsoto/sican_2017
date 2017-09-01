#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from usuarios.models import User
from rest.serializers import UserSerializer, MensajeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from inbox.models import Mensaje
from django_datatables_view.base_datatable_view import BaseDatatableView
from administrativos.models import Administrativo, Soporte
from cargos.models import Cargo
from django.db.models import Q
from usuarios.models import User
from permisos_sican.models import UserPermissionSican
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rh.models import TipoSoporte
from operator import itemgetter
from formadores.models import Formador
from formadores.models import Soporte as SoporteFormador
from lideres.models import Soporte as SoporteLider
from negociadores.models import Soporte as SoporteNegociador
from departamentos.models import Departamento
from municipios.models import Municipio
from secretarias.models import Secretaria
from rest_framework.permissions import AllowAny
from formadores.models import SolicitudTransporte
from informes.models import InformesExcel
from django.http import HttpResponse
from informes.tasks import formadores, formadores_soportes, preinscritos, transportes, cronograma_general, cronograma_lider
from informes.tasks import lideres, lideres_soportes, encuesta_percepcion_inicial, radicados, pagos_mensual, reporte_requerimientos_contratacion
from informes.tasks import acumulado_tipo_1,acumulado_tipo_2,acumulado_tipo_3,acumulado_tipo_4,matriz_chequeo, matriz_chequeo_formador, zip_ss
from informes.tasks import reporte_legalizacion_contrato_formadores
from encuestas.models import PercepcionInicial
from productos.models import Diplomado, Nivel, Sesion, Entregable
from formacion.models import EntradaCronograma
import datetime
from formacion.models import Semana
from isoweek import Week
from lideres.models import Lideres
from preinscripcion.models import DocentesPreinscritos
from radicados.models import RadicadoRetoma
from acceso.models import Retoma
from matrices.models import Beneficiario
from radicados.models import Radicado
from formacion.models import Grupos
from productos.models import Contratos, ValorEntregable
from django.db.models import Sum
from formadores.models import Revision
from formadores.models import Cortes
from negociadores.models import Negociador
from rh.models import RequerimientoPersonal
from rest_framework.renderers import JSONRenderer
from matrices.models import CargaMasiva
from evidencias.models import Evidencia
from requerimientos.models import Requerimiento
from evidencias.models import Red, CargaMasiva as CargaMasivaEvidencias
from django.utils.timezone import localtime
from informes.tasks import zip_hv, zip_contrato, actividades_virtuales
from informes.tasks import descargas_certificados_escuelatic, progreso_listados_actas, matriz_chequeo_actividad, progreso_listados_actas_aprobadas
from vigencia2017.tasks import matriz_chequeo_vigencia_2017
from evidencias.models import Subsanacion
from django.db.models import Sum
from informes.tasks import progreso_virtuales, progreso_virtuales_aprobadas,aprobados_niveles
from evidencias.tasks import build_consolidado_red, build_consolidado_aprobacion_red
from formadores.models import Contrato
from django.utils.timezone import localtime
from formadores.models import SolicitudSoportes as SolicitudSoportesFormador
from lideres.models import Contrato as ContratoLider
from lideres.models import SolicitudSoportes as SolicitudSoportesLider
from negociadores.models import Contrato as ContratoNegociador
from negociadores.models import SolicitudSoportes as SolicitudSoportesNegociador
from administrativos.models import Contrato as ContratoAdministrativo
from informes.tasks import matriz_chequeo_compilada, reporte_sed_bogota
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest.serializers import BeneficiarioSerializer
import json
from formadores.models import CohortesFormadores
from informes.tasks import matriz_chequeo_virtual_compilada
from beneficiarios.models import GruposBeneficiarios
from beneficiarios.models import BeneficiarioVigencia
from vigencia2017.models import DaneSEDE
from vigencia2017.models import Grupos as GruposVigencia2017
from vigencia2017.models import Beneficiario as BeneficiarioVigencia2017
from vigencia2017.models import TipoContrato, ValorEntregableVigencia2017
from django.db.models import Sum
from vigencia2017.models import CargaMatriz
from vigencia2017.models import Beneficiario as BeneficiarioVigencia2017
from vigencia2017.models import BeneficiarioCambio as BeneficiarioCambioVigencia2017
from collections import OrderedDict
from vigencia2017.models import Evidencia as EvidenciaVigencia2017
from vigencia2017.models import Red as RedVigencia2017RedVigencia2017
from vigencia2017.tasks import matriz_valores_vigencia_2017, matriz_chequeo_vigencia_2017_total, matriz_valores_vigencia_2017_total
from vigencia2017.models import Red as RedVigencia2017
# Create your views here.


#----------------------------------------------------- REST ------------------------------------------------------------

class UserPermissionList(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        perms_user = list(user.get_all_permissions())

        categories = {
            'adminuser':{'name':'Usuarios',
                  'icon':'icons:account-circle',
                  'id':'usuarios',
                  'links':[]
            },
            'rh':{'name':'Recursos Humanos',
                  'icon':'icons:accessibility',
                  'id':'rh',
                  'links':[]
            },
            'bases':{'name':'Bases de datos',
                  'icon':'icons:dashboard',
                  'id':'bases',
                  'links':[]
            },
            'financiera':{'name':'Financiera',
                  'icon':'icons:payment',
                  'id':'financiera',
                  'links':[]
            },
            'informes':{'name':'Mis informes',
                  'icon':'icons:assessment',
                  'id':'informes',
                  'links':[]
            },
            'formacion':{'name':'Formación',
                  'icon':'icons:language',
                  'id':'formacion',
                  'links':[]
            },
            'encuestas':{'name':'Encuestas',
                  'icon':'icons:assessment',
                  'id':'encuestas',
                  'links':[]
            },
            'productos':{'name':'Estrategia ETIC@',
                  'icon':'icons:group-work',
                  'id':'productos',
                  'links':[]
            },
            'acceso':{'name':'Acceso',
                  'icon':'icons:chrome-reader-mode',
                  'id':'acceso',
                  'links':[]
            },
            'matrices':{'name':'Matrices',
                  'icon':'icons:timeline',
                  'id':'matrices',
                  'links':[]
            },
            'evidencias':{'name':'Evidencias',
                  'icon':'icons:view-quilt',
                  'id':'evidencias',
                  'links':[]
            },
            'requerimientos':{'name':'Requerimientos',
                  'icon':'icons:gavel',
                  'id':'requerimientos',
                  'links':[]
            },
            'formadores':{'name':'Formadores',
                  'icon':'icons:face',
                  'id':'formadores',
                  'links':[]
            },
            'lideres':{'name':'Lideres regionales',
                  'icon':'hardware:computer',
                  'id':'lideres',
                  'links':[]
            },
            'negociadores':{'name':'Negociadores',
                  'icon':'icons:gavel',
                  'id':'negociadores',
                  'links':[]
            },
            'contratos':{'name':'Contratos',
                  'icon':'icons:description',
                  'id':'contratos',
                  'links':[]
            },
            'seguridad_social':{'name':'Seguridad Social',
                  'icon':'image:healing',
                  'id':'seguridad_social',
                  'links':[]
            },
            'beneficiarios':{'name':'Mis Beneficiarios',
                  'icon':'icons:face',
                  'id':'beneficiarios',
                  'links':[]
            },
            'vigencia_2017': {'name': 'Vigencia 2017',
                              'icon': 'icons:verified-user',
                              'id': 'vigencia_2017',
                              'links': []
            },

        }

        links = {
            'vigencia_2017_reds': {
                'ver': {'name': 'Formatos RED', 'link': '/vigencia2017/reds/'}
            },
            'vigencia_2017_cedula_beneficiario': {
                'ver': {'name': 'Cedula de beneficiario', 'link': '/vigencia2017/evidencias/cedula/'}
            },
            'vigencia_2017_codigos': {
                'ver': {'name': 'Codigos de soporte', 'link': '/vigencia2017/evidencias/codigos/'}
            },
            'vigencia_2017_cargar_matriz': {
                'ver': {'name': 'Carga de matriz', 'link': '/vigencia2017/cargar_matriz/'}
            },
            'vigencia_2017_valor_contratos': {
                'ver': {'name': 'Valor contratos', 'link': '/vigencia2017/valor_contratos/'}
            },
            'vigencia_2017_grupos': {
                'ver': {'name': 'Grupos de formación', 'link': '/vigencia2017/grupos/'}
            },
            'vigencia_2017_dane': {
                'ver': {'name': 'Códigos DANE', 'link': '/vigencia2017/codigosdane/'}
            },
            'beneficiarios_registrar':{
                'ver':{'name':'Registrar beneficiarios','link':'/beneficiarios/'}
            },
            'evidencias': {
                'ver': {'name': 'Registrar beneficiarios', 'link': '/beneficiarios/'}
            },
            'contratos_legalizar':{
                'ver':{'name':'Legalización de contratos','link':'/contratos/legalizacion/'}
            },
            'ss_seguridad_social':{
                'ver':{'name':'Soportes de seguridad social','link':'/contratos/seguridadsocial/'}
            },
            'seguridadsocial_lideres':{
                'ver':{'name':'Soportes de seguridad social','link':'/lideres/seguridadsocial/'}
            },
            'seguridadsocial_negociadores':{
                'ver':{'name':'Soportes de seguridad social','link':'/negociadores/seguridadsocial/'}
            },
            'rh_contratacion':{
                'ver':{'name':'Contratación','link':'/rh/contratacion/'}
            },
            'rh_personal':{
                'ver':{'name':'Personal','link':'/rh/personal/'}
            },
            'subsanacion':{
                'ver':{'name':'Subsanación de evidencias','link':'/evidencias/subsanacion/'}
            },
            'ple':{
                'ver':{'name':'PLE','link':'/evidencias/ple/'}
            },
            'cedula_beneficiario':{
                'ver':{'name':'Cedula beneficiario','link':'/evidencias/cedula/'}
            },
            'codigos_evidencia':{
                'ver':{'name':'Actividades','link':'/evidencias/actividades/'}
            },
            'auxiliares':{
                'ver':{'name':'Rendimiento carga de evidencias','link':'/evidencias/rendimiento/'}
            },
            'diplomas':{
                'ver':{'name':'Diploma EscuelaTIC','link':'/formacion/diplomas/escuelatic/'}
            },
            'proyecto':{
                'ver':{'name':'Delegación de requerimientos','link':'/requerimientos/delegacion/'}
            },
            'requerimientosrhrespuesta':{
                'ver':{'name':'Requerimientos de contratación','link':'/rh/requerimientoscontratacion/'}
            },
            'requerimientosrh':{
                'ver':{'name':'Requerimientos de contratación','link':'/formacion/requerimientoscontratacion/'}
            },
            'cortes':{
                'ver':{'name':'Cortes de pago','link':'/financiera/cortes/'}
            },
            'gruposformacion':{
                'ver':{'name':'Grupos de formación','link':'/formacion/grupos/'}
            },
            'cargamasiva':{
                'ver':{'name':'Carga masiva','link':'/matrices/cargamasiva/'}
            },
            'general':{
                'ver':{'name':'Carga general','link':'/evidencias/general/'}
            },
            'codigos':{
                'ver':{'name':'Codigos de soporte','link':'/evidencias/codigos/'}
            },
            'red':{
                'ver':{'name':'Formatos RED','link':'/evidencias/reds/'}
            },
            'cargamasivaevidencias':{
                'ver':{'name':'Carga masiva de evidencias','link':'/evidencias/cargamasiva/'}
            },
            'matricesdiplomados':{
                'ver_innovatic':{'name':'Matriz InnovaTIC','link':'/matrices/diplomados/innovatic/'},
                'ver_tecnotic':{'name':'Matriz TecnoTIC','link':'/matrices/diplomados/tecnotic/'},
                'ver_directic':{'name':'Matriz DirecTIC','link':'/matrices/diplomados/directic/'},
                'ver_escuelatic':{'name':'Matriz EscuelaTIC','link':'/matrices/diplomados/escuelatic/'},
            },
            'contratos':{
                'ver':{'name':'Contratos','link':'/financiera/contratos/'}
            },
            'retoma':{
                'ver':{'name':'Retoma','link':'/acceso/retoma/'}
            },
            'radicadosretoma':{
                'ver':{'name':'Radicados retoma','link':'/acceso/radicadosretoma/'}
            },
            'cronogramafinanciera':{
                'ver':{'name':'Cronograma de formación','link':'/financiera/cronograma/'}
            },
            'cronograma':{
                'ver':{'name':'Cronograma de formación','link':'/formacion/cronograma/'}
            },
            'transportesformacion':{
                'ver':{'name':'Solicitudes de transporte','link':'/formacion/transportes/'}
            },
            'sesiones':{
                'ver':{'name':'Sesiones','link':'/estrategia/sesiones/'}
            },
            'niveles':{
                'ver':{'name':'Niveles','link':'/estrategia/niveles/'}
            },
            'diplomados':{
                'ver':{'name':'Diplomados','link':'/estrategia/diplomados/'}
            },
            'entregables':{
                'ver':{'name':'Entregables','link':'/estrategia/entregables/'}
            },
            'revision':{
                'ver':{'name':'Revisión documental','link':'/formacion/revision/'}
            },
            'percepcioninicial':{
                'ver':{'name':'Percepción inicial y detección de necesidades','link':'/encuestas/resultados/percepcioninicial/'}
            },
            'respuestaspercepcioninicial':{
                'ver':{'name':'Respuestas percepción inicial','link':'/encuestas/respuestas/percepcioninicial/'}
            },
            'permisos':{
                'ver':{'name':'Permisos','link':'/adminuser/permisos/'}
            },
            'usuarios':{
                'ver':{'name':'Usuarios','link':'/adminuser/usuarios/'}
            },
            'grupos':{
                'ver':{'name':'Grupos','link':'/adminuser/grupos/'}
            },
            'interventoria_formadores':{
                'ver':{'name':'Consolidado Hv y Contratos','link':'/rh/consolidadoformadores/'}
            },
            'departamentos':{
                'ver':{'name':'Departamentos','link':'/bases/departamentos/'}
            },
            'municipios':{
                'ver':{'name':'Municipios','link':'/bases/municipios/'}
            },
            'secretarias':{
                'ver':{'name':'Secretarias de educación','link':'/bases/secretarias/'}
            },
            'radicados':{
                'ver':{'name':'Radicados','link':'/bases/radicados/'}
            },
            'transportes':{
                'ver':{'name':'Solicitudes de transporte','link':'/financiera/transportes/'}
            },
            'excel':{
                'ver':{'name':'Informes en excel','link':'/informes/excel/'}
            },
            'preinscritos':{
                'ver':{'name':'Docentes preinscritos','link':'/formacion/preinscritos/'}
            },
        }




        perms_response = []
        perms_dict = {}

        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        permissions = Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms).values_list('codename',flat=True)
        app = 'permisos_sican.'

        array_tuple = []

        for perm_user in perms_user:

            if perm_user.replace(app,'') in permissions:
                category, links_group, link = perm_user.replace(app,'').split('.')
                if links_group in links:
                    if link in links[links_group]:
                        array_tuple.append(([category,links_group,link],categories[category]['name'],links[links_group][link]['name']))
                        array_tuple.sort(key=itemgetter(1,2))

        for perm in array_tuple:
            perms_dict[perm[0][0]] = categories[perm[0][0]]
            perms_dict[perm[0][0]]['links'].append(links[perm[0][1]][perm[0][2]])


        for key, value in perms_dict.iteritems():
            perms_response.append((key,value,categories[key]['name']))
            perms_response.sort(key=itemgetter(2))

        r = []

        for res in perms_response:
            r.append(res[1])




        return Response(r)

class CodigosDaneList(BaseDatatableView):
    """
    0.id
    1.dane_sede
    2.nombre_sede
    3.dane_ie
    4.nombre_ie
    5.municipio
    6.secretaria
    7.zona
    """
    model = DaneSEDE
    columns = ['id', 'dane_sede', 'nombre_sede', 'dane_ie', 'nombre_ie', 'municipio', 'secretaria','zona']

    order_columns = ['dane_sede', 'nombre_sede', 'dane_ie', 'nombre_ie']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(dane_sede__icontains=search) | Q(municipio__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.dane_sede,
                item.nombre_sede,
                item.dane_ie,
                item.nombre_ie,
                item.municipio.nombre,
                item.secretaria.nombre,
                item.zona,
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.editar'),
            ])
        return json_data

class ValorContratosList(BaseDatatableView):
    """

    """
    model = TipoContrato
    columns = ['id', 'nombre']

    order_columns = ['nombre']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            diplomados = []

            for diplomado in item.diplomados.all():
                valor = ValorEntregableVigencia2017.objects.filter(tipo_contrato=item).filter(entregable__sesion__nivel__diplomado = diplomado).aggregate(Sum('valor'))['valor__sum']
                #valor = item.entregables.filter(entregable__sesion__nivel__diplomado = diplomado).aggregate(Sum('valor'))['valor__sum']
                if valor == None:
                    valor = 0
                diplomados.append({'nombre': diplomado.nombre, 'id': diplomado.id, 'valor': valor})



            json_data.append([
                item.id,
                item.nombre,
                diplomados,
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.editar'),
            ])
        return json_data

class Vigencia2017GruposList(BaseDatatableView):
    """
    0.id
    1.formador
    2.codigo_ruta
    3.get_municipios_string
    4.contrato
    5.permiso_editar
    """
    model = Contrato
    columns = ['id', 'formador','codigo_ruta']

    order_columns = ['formador','codigo_ruta']
    max_display_length = 100

    def get_initial_queryset(self):
        return Contrato.objects.filter(vigencia = "vigencia2017").exclude(tipo_contrato_id=None)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) | Q(formador__cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.formador.get_full_name(),
                item.nombre,
                GruposVigencia2017.objects.filter(contrato = item).count(),
                item.codigo_ruta,
                item.get_municipios_list(),
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.editar'),
            ])
        return json_data

class Vigencia2017ContratoList(BaseDatatableView):
    """
    0.id

    """
    model = GruposVigencia2017
    columns = ['id', 'numero', 'diplomado']

    order_columns = ['numero', 'diplomado']
    max_display_length = 100

    def get_initial_queryset(self):
        return GruposVigencia2017.objects.filter(contrato__id = self.kwargs['id_contrato'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(diplomado__nombre__icontains=search) | Q(numero__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.get_nombre_grupo(),
                item.diplomado.nombre,
                BeneficiarioVigencia2017.objects.filter(grupo = item).count(),
                item.no_conectividad,
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.editar'),
            ])
        return json_data

class CargaMatrizList(BaseDatatableView):
    """
    0.id

    """
    model = CargaMatriz
    columns = ['id', 'usuario', 'fecha']

    order_columns = ['id', 'usuario', 'fecha']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(id = search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.usuario.get_full_name_string(),
                item.fecha,
                item.get_archivo_url(),
                item.get_resultado_url(),
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.editar'),
            ])
        return json_data


class Vigencia2017BeneficiariosList(BaseDatatableView):
    """
    0.id
    """
    model = BeneficiarioVigencia2017
    columns = ['id', 'cedula', 'nombres', 'apellidos', 'dane_sede']

    order_columns = ['cedula', 'nombres', 'apellidos', 'dane_sede']
    max_display_length = 100

    def get_initial_queryset(self):
        return self.model.objects.filter(grupo__id = self.kwargs['id_grupo'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(cedula__icontains=search) | Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(dane_sede__dane_sede__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.cedula,
                item.nombres,
                item.apellidos,
                item.dane_sede.dane_sede if item.dane_sede != None else 'N/A',
                item.grupo.get_nombre_grupo(),
                item.correo,
                item.telefono_fijo,
                item.telefono_celular,
                item.area,
                item.grado,
                item.genero,
                item.dane_sede.nombre_sede if item.dane_sede != None else 'N/A',
                item.dane_sede.dane_ie if item.dane_sede != None else 'N/A',
                item.dane_sede.nombre_ie if item.dane_sede != None else 'N/A',
                item.dane_sede.municipio.nombre + ', ' + item.dane_sede.municipio.departamento.nombre if item.dane_sede != None else item.municipio.nombre + ', ' + item.municipio.departamento.nombre,
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.editar'),
            ])
        return json_data




class ListaSoportesVigencia2017(BaseDatatableView):
    """
    0.id
    1.beneficiarios
    2.aprobados
    3.archivo
    4.editar
    5.eliminar
    """
    model = EvidenciaVigencia2017
    columns = ['id']

    order_columns = ['id','id']
    max_display_length = 100

    def get_initial_queryset(self):
        return self.model.objects.filter(contrato__id = self.kwargs['id_contrato'],entregable__id = self.kwargs['id_entregable'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            baneficiarios_cargados = []
            baneficiarios_validados = []
            baneficiarios_rechazados = []

            for beneficiario in item.beneficiarios_cargados.all():
                if beneficiario != None:
                    baneficiarios_cargados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.grupo.get_nombre_grupo()])

            for beneficiario in item.beneficiarios_validados.all():
                if beneficiario != None:
                    baneficiarios_validados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.grupo.get_nombre_grupo()])

            for beneficiario in item.beneficiarios_rechazados.all():
                if beneficiario != None:
                    baneficiarios_rechazados.append([beneficiario.beneficiario_rechazo.get_full_name(),beneficiario.beneficiario_rechazo.cedula,beneficiario.beneficiario_rechazo.grupo.get_nombre_grupo(),beneficiario.observacion])


            json_data.append([
                item.id,
                item.get_beneficiarios_cantidad(),
                item.get_validados_cantidad(),
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_evidencias.editar') if item.red_id == None else False,
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_evidencias.eliminar') if item.red_id == None else False,
                baneficiarios_cargados,
                baneficiarios_validados,
                baneficiarios_rechazados
            ])
        return json_data


class PendientesMatrizList(BaseDatatableView):
    """
    0.id
    """
    model = BeneficiarioCambioVigencia2017
    columns = ['id', 'cedula', 'nombres', 'apellidos', 'dane_sede']

    order_columns = ['cedula', 'nombres', 'apellidos', 'dane_sede']
    max_display_length = 100

    def get_initial_queryset(self):
        return self.model.objects.filter(masivo__id=self.kwargs['id_masivo'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(cedula__icontains=search) | Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(
                dane_sede__dane_sede__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.cedula,
                item.nombres,
                item.apellidos,
                item.dane_sede.dane_sede,
                item.grupo.get_nombre_grupo(),
                item.correo,
                item.telefono_fijo,
                item.telefono_celular,
                item.area,
                item.grado,
                item.genero,
                item.dane_sede.nombre_sede,
                item.dane_sede.dane_ie,
                item.dane_sede.nombre_ie,
                item.dane_sede.municipio.nombre + ', ' + item.dane_sede.municipio.departamento.nombre,
                self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.editar'),
            ])
        return json_data

class Vigencia2017TreeDiplomado(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id_contrato, id_grupo):

        grupo = GruposVigencia2017.objects.get(id=id_grupo)
        r = []

        nivel_count = 0
        data = {}

        for entregable in Entregable.objects.filter(sesion__nivel__diplomado = grupo.diplomado).order_by('numero'):
            nombre_nivel = entregable.sesion.nivel.nombre
            nombre_sesion = entregable.sesion.nombre

            if nombre_nivel not in data.keys():
                data[nombre_nivel] = {'position':nivel_count,'sesiones':{},'count':0}
                nivel_count += 1


            if nombre_sesion not in data[nombre_nivel]['sesiones'].keys():
                data[nombre_nivel]['sesiones'][nombre_sesion] = {'position': data[nombre_nivel]['count']}
                data[nombre_nivel]['count'] += 1

            if 'entregables' not in data[nombre_nivel]['sesiones'][nombre_sesion].keys():
                data[nombre_nivel]['sesiones'][nombre_sesion]['entregables'] = {}

            data[nombre_nivel]['sesiones'][nombre_sesion]['entregables'][entregable.numero] = {'nombre':entregable.nombre,'id':entregable.id,'numero':entregable.numero}


        data = OrderedDict(sorted(data.items(), key=lambda x: x[1]['position']))

        for nivel in data.keys():
            sesiones = OrderedDict(sorted(data[nivel]['sesiones'].items(), key=lambda x: x[1]['position']))
            childs = []
            for sesion in sesiones.keys():
                entregables = OrderedDict(sorted(data[nivel]['sesiones'][sesion]['entregables'].items()))
                childs_entregables = []

                for entregable in entregables.keys():
                    nombre = data[nivel]['sesiones'][sesion]['entregables'][entregable]['nombre']
                    id = data[nivel]['sesiones'][sesion]['entregables'][entregable]['id']
                    numero = data[nivel]['sesiones'][sesion]['entregables'][entregable]['numero']
                    childs_entregables.append({'text':str(numero)+": "+nombre,'icon':'glyphicon glyphicon-file','href':'id/'+str(id)+'/'})

                childs.append({'text':sesion,'nodes':childs_entregables})
            r.append({'text':nivel,'state':{'expanded':False},'nodes':childs})



        return Response(r)
#-----------------------------------------------------------------------------------------------------------------------

class ResultadosPercepcionInicial(APIView):
    """
    Retorna los resultados de la encuesta de percepcion inicial.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        encuestas = PercepcionInicial.objects.all()

        response = {'0':encuestas.count(),
                    '1':{'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'14':0,'15':0,},
                    '2':{'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0},
                    '3':{'si':0,'no':0},
                    '4':{'1':0,'2':0,'3':0,'4':0},
                    '5':{'1':0,'2':0,'3':0,'4':0},
                    '6':{'1':0,'2':0,'3':0,'4':0,'5':0},
                    '7':{'1':0,'2':0,'3':0,'4':0},
                    '8':{'1':0,'2':0,'3':0,'4':0},
                    '9':{'si':0,'no':0},
                    '10':{'1':0,'2':0,'3':0,'4':0},
                    '11':{'1':0,'2':0,'3':0,'4':0},
                    '12':{'si':0,'no':0},
                    '13':{'1':0,'2':0,'3':0,'4':0},
                    '14':{'si':0,'no':0},
                    '15':{'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0},
        }

        for encuesta in encuestas:
            response['1'][encuesta.area] += 1
            antiguedad = int(encuesta.antiguedad)

            if antiguedad > 0 and antiguedad <= 5:
                response['2']['1'] += 1
            if antiguedad > 5 and antiguedad <= 10:
                response['2']['2'] += 1
            if antiguedad > 10 and antiguedad <= 15:
                response['2']['3'] += 1
            if antiguedad > 15 and antiguedad <= 20:
                response['2']['4'] += 1
            if antiguedad > 20 and antiguedad <= 25:
                response['2']['5'] += 1
            if antiguedad > 25 and antiguedad <= 30:
                response['2']['6'] += 1
            if antiguedad > 30 and antiguedad <= 35:
                response['2']['7'] += 1
            if antiguedad > 35 and antiguedad <= 40:
                response['2']['8'] += 1
            if antiguedad > 40 and antiguedad <= 45:
                response['2']['9'] += 1
            if antiguedad > 45 and antiguedad <= 50:
                response['2']['10'] += 1

            if encuesta.pregunta_1 == 'Si':
                response['3']['si'] += 1
            else:
                response['3']['no'] += 1

            if encuesta.pregunta_2 != '':
                response['4'][encuesta.pregunta_2] += 1
            if encuesta.pregunta_3 != '':
                response['5'][encuesta.pregunta_3] += 1
            if encuesta.pregunta_4 != '':
                response['6'][encuesta.pregunta_4] += 1
            if encuesta.pregunta_5 != '':
                response['7'][encuesta.pregunta_5] += 1
            if encuesta.pregunta_6 != '':
                response['8'][encuesta.pregunta_6] += 1

            if encuesta.pregunta_7 != '':
                if encuesta.pregunta_7 == 'Si':
                    response['9']['si'] += 1
                else:
                    response['9']['no'] += 1
            if encuesta.pregunta_9 != '':
                response['10'][encuesta.pregunta_8] += 1
            if encuesta.pregunta_9 != '':
                response['11'][encuesta.pregunta_9] += 1
            if encuesta.pregunta_10 != '':
                if encuesta.pregunta_10 == 'Si':
                    response['12']['si'] += 1
                else:
                    response['12']['no'] += 1
            if encuesta.pregunta_11 != '':
                response['13'][encuesta.pregunta_11] += 1
            if encuesta.pregunta_12 != '':
                if encuesta.pregunta_12 == 'Si':
                    response['14']['si'] += 1
                else:
                    response['14']['no'] += 1

            if encuesta.pregunta_13 != '':
                escala = int(encuesta.pregunta_13)

                if escala > 0 and escala <= 10:
                    response['15']['1'] += 1
                if escala > 10 and escala <= 20:
                    response['15']['2'] += 1
                if escala > 20 and escala <= 30:
                    response['15']['3'] += 1
                if escala > 30 and escala <= 40:
                    response['15']['4'] += 1
                if escala > 40 and escala <= 50:
                    response['15']['5'] += 1
                if escala > 50 and escala <= 60:
                    response['15']['6'] += 1
                if escala > 60 and escala <= 70:
                    response['15']['7'] += 1
                if escala > 70 and escala <= 80:
                    response['15']['8'] += 1
                if escala > 80 and escala <= 90:
                    response['15']['9'] += 1
                if escala > 90 and escala <= 100:
                    response['15']['10'] += 1

        return Response(response)

class ReportesView(APIView):
    """
    Retorna la informacion de los usuarios excluyendo al que realiza el request.
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        id_accion = request._request.GET['action']

        if id_accion == '1':
            x = formadores.delay(request.user.email)
        if id_accion == '2':
            x = formadores_soportes.delay(request.user.email)
        if id_accion == '3':
            x = preinscritos.delay(request.user.email)
        if id_accion == '4':
            x = transportes.delay(request.user.email)
        if id_accion == '5':
            semana_id = request._request.GET['semana_id']
            x = cronograma_general.delay(request.user.email,semana_id)
        if id_accion == '6':
            semana_id = request._request.GET['semana_id']
            x = cronograma_lider.delay(request.user.email,semana_id)
        if id_accion == '7':
            x = lideres.delay(request.user.email)
        if id_accion == '8':
            x = lideres_soportes.delay(request.user.email)
        if id_accion == '9':
            x = encuesta_percepcion_inicial.delay(request.user.email)
        if id_accion == '10':
            x = radicados.delay(request.user.email)
        if id_accion == '11':
            x = pagos_mensual.delay(request.user.email)

        if id_accion == '12':
            x = zip_hv.delay(request.user.email)
        if id_accion == '13':
            x = zip_contrato.delay(request.user.email)

        if id_accion == '14':
            x = reporte_requerimientos_contratacion.delay(request.user.email)

        if id_accion == '15':
            x = acumulado_tipo_1.delay(request.user.email)
        if id_accion == '16':
            x = acumulado_tipo_2.delay(request.user.email)
        if id_accion == '17':
            x = acumulado_tipo_3.delay(request.user.email)
        if id_accion == '18':
            x = acumulado_tipo_4.delay(request.user.email)
        if id_accion == '19':
            id_diplomado = request._request.GET['id_diplomado']
            x = matriz_chequeo.delay(request.user.email,id_diplomado)
        if id_accion == '20':
            id_formador = request._request.GET['id_formador']
            x = matriz_chequeo_formador.delay(request.user.email,id_formador)
        if id_accion == '21':
            x = zip_ss.delay(request.user.email)
        if id_accion == '22':
            x = descargas_certificados_escuelatic.delay(request.user.email)
        if id_accion == '23':
            x = progreso_listados_actas.delay(request.user.email)
        if id_accion == '24':
            id_actividad = request._request.GET['id_actividad']
            x = matriz_chequeo_actividad.delay(request.user.email,id_actividad)
        if id_accion == '25':
            x = progreso_listados_actas_aprobadas.delay(request.user.email)
        if id_accion == '26':
            x = progreso_virtuales.delay(request.user.email)
        if id_accion == '27':
            x = progreso_virtuales_aprobadas.delay(request.user.email)
        if id_accion == '28':
            x = build_consolidado_red.delay(request.user.email)
        if id_accion == '29':
            x = build_consolidado_aprobacion_red.delay(request.user.email)
        if id_accion == '30':
            x = aprobados_niveles.delay(request.user.email)
        if id_accion == '31':
            x = actividades_virtuales.delay(request.user.email)
        if id_accion == '32':
            x = matriz_chequeo_compilada.delay(request.user.email)
        if id_accion == '33':
            x = reporte_sed_bogota.delay(request.user.email)
        if id_accion == '34':
            x = reporte_legalizacion_contrato_formadores.delay(request.user.email)
        if id_accion == '35':
            x = matriz_chequeo_virtual_compilada.delay(request.user.email)
        if id_accion == '36':
            id_contrato = request._request.GET['id_contrato']
            x = matriz_chequeo_vigencia_2017.delay(request.user.email,id_contrato)
        if id_accion == '37':
            id_contrato = request._request.GET['id_contrato']
            x = matriz_valores_vigencia_2017.delay(request.user.email,id_contrato)
        if id_accion == '38':
            x = matriz_chequeo_vigencia_2017_total.delay(request.user.email)
        if id_accion == '39':
            x = matriz_valores_vigencia_2017_total.delay(request.user.email)

        return HttpResponse(status=200)

class MunicipiosChainedList(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        keys = [
            'departamento',
            'departamento_natal',
            'departamento_residencia',
            'departamento_residencia_temporal',
            'departamento_origen_1','departamento_destino_1',
            'departamento_origen_2','departamento_destino_2',
            'departamento_origen_3','departamento_destino_3',
            'departamento_origen_4','departamento_destino_4',
            'departamento_origen_5','departamento_destino_5',
            'departamento_origen_6','departamento_destino_6',
            'departamento_origen_7','departamento_destino_7',
            'departamento_origen_8','departamento_destino_8',
            'departamento_origen_9','departamento_destino_9',
            'departamento_origen_10','departamento_destino_10',

        ]

        for key in keys:
            if key in request._request.GET:
                id_departamento = request._request.GET[key]

        if id_departamento == '':
            id_departamento = 0
        municipios = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

        response = {}

        for municipio in municipios:
            response[municipio[0]] = municipio[1]

        return Response(response)

class RadicadosChainedList(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            id_municipio = request._request.GET['municipio']
        except:
            id_municipio = 0
        if id_municipio == '':
            id_municipio = 0
        radicados = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        response = {}

        for radicado in radicados:
            response[radicado[0]] = radicado[1]

        return Response(response)

class Cedulas2BeneficiariosId(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        cedulas = request.query_params['cedulas'].split(',')
        ids = []
        for cedula in cedulas:
            try:
                beneficiario = Beneficiario.objects.get(cedula = cedula)
            except:
                pass
            else:
                ids.append(str(beneficiario.id))

        response = {'cedulas':ids}


        return Response(response)



class Cedulas2BeneficiariosIdVigencia2017(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        cedulas = request.query_params['cedulas'].split(',')
        ids = []
        for cedula in cedulas:
            try:
                beneficiario = BeneficiarioVigencia2017.objects.get(cedula = cedula)
            except:
                pass
            else:
                ids.append(str(beneficiario.id))

        response = {'cedulas':ids}


        return Response(response)


class GrupoCedulas2BeneficiariosIdVigencia2017(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    def get(self, request, id_grupo, format=None):

        ids = []
        for beneficiario in BeneficiarioVigencia2017.objects.filter(grupo__id=id_grupo):
            ids.append(str(beneficiario.id))

        response = {'cedulas':ids}


        return Response(response)


class GruposChainedList(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            id_formador = request._request.GET['formador']
        except:
            id_formador = 0

        if id_formador == '':
            id_formador = 0
        grupos = Grupos.objects.filter(formador__id=id_formador)

        response = {}

        for grupo in grupos:
            response[grupo.id] = unicode(grupo.formador.codigo_ruta) + "-" + grupo.nombre

        return Response(response)

class SecretariasChainedList(APIView):
    """

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        try:
            id_municipio = request._request.GET['municipio']
        except:
            return Response({})

        departamento_id = Municipio.objects.get(id=id_municipio).departamento.id
        id_municipios = Municipio.objects.filter(departamento__id = departamento_id).values_list('id',flat=True)

        secretarias = Secretaria.objects.filter(municipio__id__in = id_municipios).values_list('id','nombre')

        response = {}

        for secretaria in secretarias:
            response[secretaria[0]] = secretaria[1]

        return Response(response)

class AutocompleteRadicados(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        query = request.query_params['query']
        response = []
        q = Q(numero__startswith=query) | Q(municipio__departamento__nombre__icontains=query) |\
            Q(municipio__nombre__icontains=query) | Q(nombre_sede__icontains=query)

        for radicado in Radicado.objects.filter(q):
            response.append({'value':str(radicado.numero)+ ' - ' + radicado.municipio.nombre + ', ' +
                                     radicado.municipio.departamento.nombre + ' - ' + radicado.nombre_sede,'data':str(radicado.numero)})

        return Response({'suggestions':response})



class ContratoInfoView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        contrato = None
        data = {'vigencia':'----','municipios':'----','supervisores':'----','meta_beneficiarios':'----',
                'inscritos_contrato':'----','inscritos_grupo':'----'}
        if 'id_contrato' in request.data.keys() and 'id_grupo' in request.data.keys():
            try:
                contrato = Contrato.objects.get(id=request.data['id_contrato'])
            except:
                pass
            else:
                grupos = GruposBeneficiarios.objects.filter(contrato=contrato)
                beneficiarios = BeneficiarioVigencia.objects.filter(grupo__in = grupos)
                data['vigencia'] = contrato.vigencia
                data['municipios'] = contrato.get_municipios_list()
                data['supervisores'] = contrato.get_supervisores_list()
                data['meta_beneficiarios'] = contrato.meta_beneficiarios
                data['inscritos_contrato'] = beneficiarios.count()

                try:
                    grupo = GruposBeneficiarios.objects.get(id = request.data['id_grupo'])
                except:
                    data['inscritos_grupo'] = '----'
                else:
                    data['inscritos_grupo'] = BeneficiarioVigencia.objects.filter(grupo = grupo).count()
        elif 'id_contrato' in request.data.keys():
            try:
                contrato = Contrato.objects.get(id=request.data['id_contrato'])
            except:
                pass
            else:
                grupos = GruposBeneficiarios.objects.filter(contrato=contrato)
                beneficiarios = BeneficiarioVigencia.objects.filter(grupo__in=grupos)
                data['vigencia'] = contrato.vigencia
                data['municipios'] = contrato.get_municipios_list()
                data['supervisores'] = contrato.get_supervisores_list()
                data['meta_beneficiarios'] = contrato.meta_beneficiarios
                data['inscritos_contrato'] = beneficiarios.count()

        return Response({'contrato':data})




class AutocompleteMunicipios(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):

        query = request.query_params['query']
        response = []
        q = Q(nombre__istartswith=query)

        for municipio in Municipio.objects.filter(q):
            response.append({ 'value': municipio.nombre + ', ' + municipio.departamento.nombre })

        return Response({'suggestions':response})

class UserList(APIView):
    """
    Retorna la informacion de los usuarios excluyendo al que realiza el request.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        users = User.objects.exclude(id = request.user.id).exclude(email="AnonymousUser")
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

class UserChatList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        users = Mensaje.objects.exclude(user = request.user)
        serializer = MensajeSerializer(users,many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(request, *args, **kwargs):
        users = User.objects.filter(id=kwargs['id'])
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

class CedulaDocente(APIView):
    """
    Retorna la informacion de los usuarios excluyendo al que realiza el request.
    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None, cedula = None):
        beneficiario = Beneficiario.objects.filter(cedula = cedula)
        serializer = BeneficiarioSerializer(beneficiario,many=True)
        return Response({'cantidad':beneficiario.count(),'data':serializer.data})



class AdminUserList(BaseDatatableView):
    """
    0.id
    1.email
    2.first_name
    3.last_name
    4.is_active
    5.cargo
    6.telefono_personal
    7.correo_personal
    8.permiso para editar
    """
    model = User
    columns = ['id','email','first_name','last_name','is_active','cargo','telefono_personal','correo_personal']

    order_columns = ['id','email','first_name','last_name']
    max_display_length = 100

    def get_initial_queryset(self):
        return User.objects.exclude(email="AnonymousUser")


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.email,
                item.first_name,
                item.last_name,
                item.is_active,
                item.cargo.nombre,
                item.telefono_personal,
                item.correo_personal,
                self.request.user.has_perm('permisos_sican.adminuser.usuarios.editar'),
            ])
        return json_data

class GroupUserList(BaseDatatableView):
    """
    0.id
    1.name
    2.permissions
    3.permiso para editar
    4.permiso para eliminar
    """
    model = Group
    columns = ['id','name','permissions']

    order_columns = ['id','name']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(name__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            result = []
            permisos = Group.objects.get(id=item.id).permissions.all()
            for permiso in permisos:
                result.append(permiso.__str__())
            json_data.append([
                item.id,
                item.name,
                result,
                self.request.user.has_perm('permisos_sican.adminuser.grupos.editar'),
                self.request.user.has_perm('permisos_sican.adminuser.grupos.eliminar'),
            ])
        return json_data

class AdminUserPermissionList(BaseDatatableView):
    """
    0.id
    1.name
    2.codename
    3.permiso para editar
    4.permiso para eliminar
    """
    model = Permission
    columns = ['id','name','codename']
    order_columns = ['id','name','codename']
    max_display_length = 100

    def get_initial_queryset(self):
        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        return Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.name,
                item.codename,
                self.request.user.has_perm('permisos_sican.adminuser.permisos.editar'),
                self.request.user.has_perm('permisos_sican.adminuser.permisos.eliminar')
            ])
        return json_data

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(codename__icontains=search) | Q(name__icontains=search)
            qs = qs.filter(q)
        return qs



class FormadoresConsolidadoRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.fecha_contratacion
    9.fecha_terminacion
    10.banco
    11.tipo_cuenta
    12.numero_cuenta
    13.eps
    14.pension
    15.arl
    """
    model = Formador
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'fecha_contratacion','fecha_terminacion','banco','tipo_cuenta','numero_cuenta','eps',
               'pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            region_str = ''
            for region in item.region.values_list('numero',flat=True):
                region_str = region_str + str(region) + ','
            region_str = region_str[:-1]

            if item.banco != None:
                banco = item.banco.nombre
            else:
                banco = ''

            try:
                hv = SoporteFormador.objects.exclude(oculto = True).get(formador = item,tipo__id = 3).get_archivo_url()
            except:
                hv = ''

            try:
                contrato = SoporteFormador.objects.exclude(oculto = True).get(formador = item,tipo__id = 10).get_archivo_url()
            except:
                contrato = ''

            json_data.append([
                item.id,
                item.nombres + " " + item.apellidos,
                item.cargo.nombre,
                region_str,
                item.cedula,
                item.correo_personal,
                item.celular_personal,
                item.profesion,
                item.fecha_contratacion,
                item.fecha_terminacion,
                banco,
                item.tipo_cuenta,
                item.numero_cuenta,
                item.eps,
                item.pension,
                item.arl,
                hv,
                contrato
            ])
        return json_data



class DepartamentosList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.codigo_departamento
    3.codigo_auditoria
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Departamento
    columns = ['id','nombre','codigo_departamento']

    order_columns = ['id','nombre','codigo_departamento']
    max_display_length = 100

    def get_initial_queryset(self):
        return Departamento.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search) | Q(codigo_departamento__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.codigo_departamento,
                item.codigo_auditoria,
                self.request.user.has_perm('permisos_sican.bases.departamentos.editar'),
                self.request.user.has_perm('permisos_sican.bases.departamentos.eliminar'),
            ])
        return json_data

class MunicipiosList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.departamento
    3.codigo_municipio
    4.codigo_auditoria
    5.permiso para editar
    6.permiso para eliminar
    """
    model = Municipio
    columns = ['id','nombre','departamento','codigo_municipio','codigo_auditoria']

    order_columns = ['id','nombre','departamento','codigo_municipio','codigo_auditoria']
    max_display_length = 100

    def get_initial_queryset(self):
        return Municipio.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(departamento__nombre__icontains=search) | Q(nombre__icontains=search) | Q(codigo_municipio__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.departamento.nombre,
                item.codigo_municipio,
                item.codigo_auditoria,
                self.request.user.has_perm('permisos_sican.bases.municipios.editar'),
                self.request.user.has_perm('permisos_sican.bases.municipios.eliminar'),
            ])
        return json_data

class SecretariasList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.departamento
    3.tipo
    4.direccion
    5.web
    6.permiso para editar
    7.permiso para eliminar
    """
    model = Secretaria
    columns = ['id','nombre','municipio','tipo','direccion','web']

    order_columns = ['id','nombre','municipio','tipo','direccion','web']
    max_display_length = 100

    def get_initial_queryset(self):
        return Secretaria.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(municipio__departamento__nombre__icontains=search) | Q(municipio__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.municipio.departamento.nombre,
                item.tipo,
                item.direccion,
                item.web,
                self.request.user.has_perm('permisos_sican.bases.secretarias.editar'),
                self.request.user.has_perm('permisos_sican.bases.secretarias.eliminar'),
            ])
        return json_data

class RadicadosList(BaseDatatableView):
    """
    0.id
    1.numero
    2.secretaria
    3.municipio
    4.nombre_sede

    5.dane_sede
    6.tipo
    7.ubicacion
    8.permiso para editar
    9.permiso para eliminar
    """
    model = Secretaria
    columns = ['id','numero','secretaria','municipio','nombre_sede','dane_sede','tipo','ubicacion']

    order_columns = ['id','numero','secretaria','municipio','nombre_sede','dane_sede','tipo','ubicacion']
    max_display_length = 100

    def get_initial_queryset(self):
        return Radicado.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(numero__icontains=search) | Q(secretaria__nombre__icontains=search) | \
                Q(municipio__nombre__icontains=search) | Q(municipio__departamento__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.numero,
                item.secretaria.nombre,
                item.municipio.nombre,
                item.nombre_sede,
                item.dane_sede,
                item.tipo,
                item.ubicacion,
                self.request.user.has_perm('permisos_sican.bases.radicados.editar'),
                self.request.user.has_perm('permisos_sican.bases.radicados.eliminar'),
            ])
        return json_data

class SolicitudesTransporteList(BaseDatatableView):
    """
    0.formador
    1.cedula
    2.Lider
    3.id
    4.cantidad consignadas
    5.cantidad aprobadasfinanciera financiera
    6.cantidad aprobadasfinanciera lider
    7.cantidad rechazadas
    8.cantidad pendientes
    9.permiso para editar
    """
    model = Formador
    columns = ['nombres','cedula','lider','id']

    order_columns = ['nombres','cedula','lider','id']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search == "Aprobadas lideres":
            solicitudes = SolicitudTransporte.objects.filter(estado="aprobado_lider").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Consignadas":
            solicitudes = SolicitudTransporte.objects.filter(estado="consignado").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Aprobadas financiera":
            solicitudes = SolicitudTransporte.objects.filter(estado="aprobado").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Rechazadas":
            solicitudes = SolicitudTransporte.objects.filter(estado="rechazado").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Pendientes":
            solicitudes = SolicitudTransporte.objects.filter(estado="revision").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        else:
            if search:
                q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | \
                    Q(cedula__icontains=search) | Q(lider__first_name__icontains=search) | Q(lider__last_name__icontains=search)
                qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            solicitudes = SolicitudTransporte.objects.filter(formador__cedula=item.cedula)
            json_data.append([
                item.get_full_name(),
                item.cedula,
                item.lider.get_full_name_string() if item.lider != None else '',
                item.id,
                solicitudes.filter(estado="consignado").count(),
                solicitudes.filter(estado="aprobado").count(),
                solicitudes.filter(estado="aprobado_lider").count(),
                solicitudes.filter(estado="rechazado").count(),
                solicitudes.filter(estado="revision").count(),
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
            ])
        return json_data

class InformesExcelList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.creacion
    3.archivo
    4.permiso para editar
    5.permiso para eliminar
    """
    model = InformesExcel
    columns = ['id','nombre','creacion','archivo']

    order_columns = ['id','nombre','creacion','archivo']
    max_display_length = 100

    def get_initial_queryset(self):
        return InformesExcel.objects.filter(usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.creacion,
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
                self.request.user.has_perm('permisos_sican.financiera.transportes.eliminar'),
            ])
        return json_data

class PreinscritosList(BaseDatatableView):
    """
    0.id
    1.primer apellido
    2.cargo
    3.departamento
    4.verificado
    5.cedula
    6.correo
    7.telefono_fijo
    8.telefono_celular
    9.radicado
    10.fecha
    11.permiso para editar
    12.permiso para eliminar
    """
    model = DocentesPreinscritos
    columns = ['id','primer_apellido','cargo','departamento','verificado']

    order_columns = ['id','primer_apellido','cargo','departamento','verificado']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(primer_apellido__icontains=search) | Q(segundo_apellido__icontains=search) |\
                Q(primer_nombre__icontains=search) | Q(segundo_nombre__icontains=search) |\
                Q(cargo__icontains=search) | Q(cargo__icontains=search) | Q(cedula__icontains=search) |\
                Q(departamento__nombre__icontains=search) | Q(municipio__nombre__icontains=search) |\
                Q(radicado__numero__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.primer_apellido + ' ' + item.segundo_apellido + ' ' + item.primer_nombre + ' ' + item.segundo_nombre,
                item.cargo,
                item.departamento.nombre + ', ' + item.municipio.nombre,
                'Si' if item.verificado else 'No',
                item.cedula,
                item.correo,
                item.telefono_fijo,
                item.telefono_celular,
                item.radicado.numero,
                item.fecha,
                self.request.user.has_perm('permisos_sican.formacion.preinscritos.editar'),
                self.request.user.has_perm('permisos_sican.formacion.preinscritos.eliminar'),
            ])
        return json_data

class DiplomadosList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.permiso para editar
    4.permiso para eliminar
    """
    model = Diplomado
    columns = ['id','nombre','numero']

    order_columns = ['nombre','numero']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = search.upper()
            q = Q(nombre__icontains=search) | Q(numero__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                self.request.user.has_perm('permisos_sican.productos.diplomados.editar'),
                self.request.user.has_perm('permisos_sican.productos.diplomados.eliminar'),
            ])
        return json_data

class NivelesList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.diplomado
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Nivel
    columns = ['id','nombre','numero','diplomado']

    order_columns = ['nombre','numero','diplomado']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize()) | Q(numero__icontains=search) | Q(diplomado__nombre__icontains=search.upper())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                item.diplomado.nombre,
                self.request.user.has_perm('permisos_sican.productos.niveles.editar'),
                self.request.user.has_perm('permisos_sican.productos.niveles.eliminar'),
            ])
        return json_data

class SesionesList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.diplomado
    4.nivel
    5.permiso para editar
    6.permiso para eliminar
    """
    model = Sesion
    columns = ['id','nombre','numero','diplomado','nivel']

    order_columns = ['nombre','numero','diplomado','nivel']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search) | Q(nivel__nombre__icontains=search) | \
                Q(nivel__diplomado__nombre__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                item.nivel.diplomado.nombre,
                item.nivel.nombre,
                self.request.user.has_perm('permisos_sican.productos.sesiones.editar'),
                self.request.user.has_perm('permisos_sican.productos.sesiones.eliminar'),
            ])
        return json_data

class EntregablesList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.diplomado
    4.nivel
    5.sesion
    6.soporte
    7.permiso para editar
    8.permiso para eliminar
    """
    model = Entregable
    columns = ['id','nombre','numero','diplomado','nivel','sesion']

    order_columns = ['nombre','numero','diplomado','nivel','sesion']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search) | Q(sesion__nivel__nombre__icontains=search.capitalize()) | \
                Q(sesion__nivel__diplomado__nombre__icontains=search.upper())

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                item.sesion.nivel.diplomado.nombre,
                item.sesion.nivel.nombre,
                item.sesion.nombre,
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.productos.entregables.editar'),
                self.request.user.has_perm('permisos_sican.productos.entregables.eliminar'),
            ])
        return json_data

class AcividadesList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.diplomado
    4.nivel
    5.sesion
    6.soporte
    7.permiso para editar
    8.permiso para eliminar
    """
    model = Entregable
    columns = ['id','nombre','numero','diplomado','nivel','sesion']

    order_columns = ['nombre','numero','diplomado','nivel','sesion']
    max_display_length = 100

    def get_initial_queryset(self):
        return Entregable.objects.filter(sesion__nivel__diplomado__id = self.kwargs['id_diplomado'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search) | Q(sesion__nivel__nombre__icontains=search.capitalize()) | \
                Q(sesion__nivel__diplomado__nombre__icontains=search.upper())

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []

        evidencias_diplomado = Evidencia.objects.filter(entregable__sesion__nivel__diplomado__id = self.kwargs['id_diplomado'])

        if self.kwargs['id_diplomado'] == '1':
            meta_r1 = 11106
            meta_r2 = 17869
        elif self.kwargs['id_diplomado'] == '2':
            meta_r1 = 1160
            meta_r2 = 1124
        elif self.kwargs['id_diplomado'] == '3':
            meta_r1 = 2860
            meta_r2 = 1298
        else:
            meta_r1 = 0
            meta_r2 = 0


        for item in qs:

            evidencias_actividad = evidencias_diplomado.filter(entregable = item).values_list('beneficiarios_cargados__id',flat = True)
            beneficiarios = Beneficiario.objects.filter(id__in = evidencias_actividad)

            cargados = evidencias_actividad.distinct().count()
            progreso = "{0:.2f}".format((float(beneficiarios.count())/float(meta_r1+meta_r2))*100.0) + "%"

            pendientes = meta_r1+ meta_r2 - cargados

            cantidad_r1 = beneficiarios.filter(formador__region__id = 1).count()
            progreso_r1 = "{0:.2f}".format((float(cantidad_r1)/float(meta_r1))*100.0) + "%"
            cantidad_r2 = beneficiarios.filter(formador__region__id = 2).count()
            progreso_r2 = "{0:.2f}".format((float(cantidad_r2)/float(meta_r2))*100.0) + "%"

            json_data.append([
                item.id,
                item.nombre,
                item.sesion.nivel.nombre + '-' + item.sesion.nombre,
                cargados,
                progreso,
                pendientes,
                cantidad_r1,
                progreso_r1,
                cantidad_r2,
                progreso_r2,
            ])
        return json_data

class SolicitudesTransporteFormacionList(BaseDatatableView):
    """
    0.formador
    1.cedula
    2.id
    3.cantidad consignadas
    4.cantidad aprobadasfinanciera financiera
    5.cantidad aprobadasfinanciera lider
    6.cantidad rechazadas
    7.cantidad pendientes
    8.permiso para editar
    """
    model = Formador
    columns = ['nombres','cedula','id']

    order_columns = ['nombres','cedula','id']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(lider = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search == "Aprobadas lideres":
            solicitudes = SolicitudTransporte.objects.filter(estado="aprobado_lider").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Consignadas":
            solicitudes = SolicitudTransporte.objects.filter(estado="consignado").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Aprobadas financiera":
            solicitudes = SolicitudTransporte.objects.filter(estado="aprobado").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Rechazadas":
            solicitudes = SolicitudTransporte.objects.filter(estado="rechazado").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        elif search == "Pendientes":
            solicitudes = SolicitudTransporte.objects.filter(estado="revision").values_list('formador__id',flat=True)
            q = Q(id__in = solicitudes)
            qs = qs.filter(q)
        else:
            if search:
                q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | \
                    Q(cedula__icontains=search)
                qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            solicitudes = SolicitudTransporte.objects.filter(formador__cedula=item.cedula)
            json_data.append([
                item.get_full_name(),
                item.cedula,
                item.id,
                solicitudes.filter(estado="consignado").count(),
                solicitudes.filter(estado="aprobado").count(),
                solicitudes.filter(estado="aprobado_lider").count(),
                solicitudes.filter(estado="rechazado").count(),
                solicitudes.filter(estado="revision").count(),
                self.request.user.has_perm('permisos_sican.financiera.transportesformacion.editar'),
            ])
        return json_data

class SolicitudesTransporteFormadorList(BaseDatatableView):
    """
    0.id
    1.formador
    2.fecha
    3.valor
    4.valor_aprobado_lider
    5.valor_aprobado
    6.desplazamientos
    7.estado
    8.archivo
    9.nombre
    10.permiso para editar
    11.permiso para eliminar
    12.permiso para cambiar estado
    """
    model = SolicitudTransporte
    columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']

    order_columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']
    max_display_length = 100

    def get_initial_queryset(self):
        estado = self.request.GET['estado']
        return SolicitudTransporte.objects.filter(formador__id=self.kwargs['id_formador']).filter(estado=estado)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) | \
                Q(formador__cedula__icontains=search) | Q(estado__icontains=search.lower())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            formador = item.formador.nombres + " " + item.formador.apellidos

            desplazamientos_response = []

            for desplazamiento in item.desplazamientos.all():
                desplazamientos_response.append([
                    desplazamiento.fecha,
                    desplazamiento.departamento_origen.nombre,
                    desplazamiento.municipio_origen.nombre,
                    desplazamiento.departamento_destino.nombre,
                    desplazamiento.municipio_destino.nombre,
                    desplazamiento.valor,
                    desplazamiento.motivo
                ])

            json_data.append([
                item.id,
                formador,
                item.creacion_date,
                item.valor,
                item.valor_aprobado_lider,
                item.valor_aprobado,
                desplazamientos_response,
                item.estado,
                item.get_archivo_url(),
                item.nombre,
                self.request.user.has_perm('permisos_sican.formacion.transportesformacion.editar'),
                self.request.user.has_perm('permisos_sican.formacion.transportesformacion.eliminar'),
                self.request.user.has_perm('permisos_sican.formacion.transportesformacion.estado'),
            ])
        return json_data

class SolicitudesTransporteFormadorFinancieraList(BaseDatatableView):
    """
    0.id
    1.formador
    2.fecha
    3.valor
    4.valor_aprobado_lider
    5.valor_aprobado
    6.desplazamientos
    7.estado
    8.archivo
    9.nombre
    10.permiso para editar
    11.permiso para eliminar
    12.permiso para cambiar estado
    """
    model = SolicitudTransporte
    columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']

    order_columns = ['id','nombre','creacion','valor','valor_aprobado_lider','valor_aprobado','estado']
    max_display_length = 100

    def get_initial_queryset(self):
        estado = self.request.GET['estado']
        return SolicitudTransporte.objects.filter(formador__id=self.kwargs['id_formador']).filter(estado=estado)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) | \
                Q(formador__cedula__icontains=search) | Q(estado__icontains=search.lower())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            formador = item.formador.nombres + " " + item.formador.apellidos

            desplazamientos_response = []

            for desplazamiento in item.desplazamientos.all():
                desplazamientos_response.append([
                    desplazamiento.fecha,
                    desplazamiento.departamento_origen.nombre,
                    desplazamiento.municipio_origen.nombre,
                    desplazamiento.departamento_destino.nombre,
                    desplazamiento.municipio_destino.nombre,
                    desplazamiento.valor,
                    desplazamiento.motivo
                ])

            json_data.append([
                item.id,
                formador,
                item.creacion_date,
                item.valor,
                item.valor_aprobado_lider,
                item.valor_aprobado,
                desplazamientos_response,
                item.estado,
                item.get_archivo_url(),
                item.nombre,
                self.request.user.has_perm('permisos_sican.financiera.transportes.editar'),
                self.request.user.has_perm('permisos_sican.financiera.transportes.eliminar'),
                self.request.user.has_perm('permisos_sican.financiera.transportes.estado'),
                localtime(item.aprobacion_lider).strftime('%d/%m/%Y %H:%M:%S') if item.aprobacion_lider != None else ''
            ])
        return json_data

class FormadoresCronogramasList(BaseDatatableView):
    """
    0.id
    1.formador
    2.cedula
    3.departamentos
    4.codigo_ruta
    5.registros
    6.permiso para editar
    """
    model = Formador
    columns = ['id','nombres','cedula']

    order_columns = ['id','nombres','cedula']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(lider = self.request.user,oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | \
                Q(cedula__icontains=search)
            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        semana = Semana.objects.get(id=self.kwargs['id_semana'])
        for item in qs:
            entradas = EntradaCronograma.objects.filter(semana=semana,formador__id = item.id)
            json_data.append([
                item.id,
                item.get_full_name(),
                item.cedula,
                item.get_departamentos_string(),
                item.codigo_ruta,
                entradas.count(),
                self.request.user.has_perm('permisos_sican.formacion.cronograma.editar'),
            ])
        return json_data

class FormadoresCronogramasFilterList(BaseDatatableView):
    """
    0.id
    1.departamento
    2.municipio
    3.secretaria
    4.grupo
    5.sedes atentidas
    6.nivel
    7.actividades presenciales
    8.beneficiados
    9.fecha
    10.institucion
    11.direccion
    12.telefono
    13.hora inicio
    14.hora finalizacion
    15.ubicacion
    16.observaciones
    17.permiso para editar
    18.permiso para eliminar
    """
    model = EntradaCronograma
    columns = ['id','departamento','municipio','secretaria','grupo','numero_sedes','nivel']

    order_columns = ['id','departamento','municipio','secretaria','grupo','numero_sedes','nivel']
    max_display_length = 100

    def get_initial_queryset(self):
        semana = Semana.objects.get(id = self.kwargs['id_semana'])
        return EntradaCronograma.objects.filter(formador__id=self.kwargs['id_formador'],semana__numero = semana.creacion.isocalendar()[1]+1)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        #if search:
        #    q = Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) | \
        #        Q(formador__cedula__icontains=search) | Q(estado__icontains=search.lower())
        #    qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.departamento.nombre,
                item.municipio.nombre,
                item.secretaria.nombre,
                item.grupo.nombre,
                item.numero_sedes,
                item.nivel.count(),
                item.actividades_entrada.count(),
                item.beneficiados,
                item.fecha,
                item.institucion,
                item.direccion,
                item.telefono,
                item.hora_inicio,
                item.hora_finalizacion,
                item.ubicacion,
                item.observaciones,
                self.request.user.has_perm('permisos_sican.formacion.cronograma.editar'),
                self.request.user.has_perm('permisos_sican.formacion.cronograma.eliminar'),
            ])
        return json_data

class SemanasList(BaseDatatableView):
    """
    0.id
    1.numero
    2.creacion
    3.rango
    4.permiso para editar
    """
    model = Semana
    columns = ['id','numero','creacion']

    order_columns = ['id','numero','creacion']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(numero__icontains=search)
            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            inicio = Week(datetime.datetime.now().isocalendar()[0],item.numero).monday()
            fin = Week(datetime.datetime.now().isocalendar()[0],item.numero).sunday()
            json_data.append([
                item.id,
                item.numero,
                item.creacion.strftime("%d de %B del %Y"),
                inicio.strftime("%d de %B del %Y") + ' - ' + fin.strftime("%d de %B del %Y"),
                self.request.user.has_perm('permisos_sican.financiera.cronogramafinanciera.editar'),
            ])
        return json_data






class SemanasFormacionList(BaseDatatableView):
    """
    0.id
    1.numero
    2.rango
    3.permiso para editar
    """
    model = Semana
    columns = ['id','numero']

    order_columns = ['id','numero']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(numero__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            inicio = Week(datetime.datetime.now().isocalendar()[0],item.numero).monday()
            fin = Week(datetime.datetime.now().isocalendar()[0],item.numero).sunday()
            json_data.append([
                item.id,
                item.numero,
                inicio.strftime("%d de %B del %Y") + ' - ' + fin.strftime("%d de %B del %Y"),
                self.request.user.has_perm('permisos_sican.formacion.cronograma.editar'),
            ])
        return json_data

class FormadoresFinancieraCronogramasList(BaseDatatableView):
    """
    0.id
    1.formador
    2.lider
    3.cedula
    4.departamentos
    5.codigo_ruta
    6.registros
    7.permiso para editar
    """
    model = Formador
    columns = ['id','nombres','lider','cedula']

    order_columns = ['nombres','lider','cedula']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.exclude(oculto = True).exclude(lider = None)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | \
                Q(cedula__icontains=search) | Q(lider__first_name__icontains=search)
            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        semana = Semana.objects.get(id=self.kwargs['id_semana'])
        for item in qs:
            entradas = EntradaCronograma.objects.filter(semana=semana,formador__id = item.id)
            json_data.append([
                item.id,
                item.get_full_name(),
                item.lider.first_name,
                item.cedula,
                item.get_departamentos_string(),
                item.codigo_ruta,
                entradas.count(),
                self.request.user.has_perm('permisos_sican.financiera.cronogramafinanciera.editar'),
            ])
        return json_data

class ResultadosPercepcionInicialList(BaseDatatableView):
    """
    0.id
    1.nombre completo
    2.cedula
    3.departamento
    4.municipio
    5.radicado
    6.permiso para editar
    7.permiso para eliminar
    """
    model = PercepcionInicial
    columns = ['id','pregunta_1','pregunta_1','pregunta_1','pregunta_1','pregunta_1']

    order_columns = ['pregunta_1','pregunta_1','pregunta_1','pregunta_1','pregunta_1']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(docente_preinscrito__primer_nombre__icontains=search) | Q(docente_preinscrito__segundo_nombre__icontains=search) | \
                Q(docente_preinscrito__primer_apellido__icontains=search) | Q(docente_preinscrito__segundo_apellido__icontains=search) | \
                Q(docente_preinscrito__departamento__nombre__icontains=search) | Q(docente_preinscrito__municipio__nombre__icontains=search)
            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.docente_preinscrito.get_full_name(),
                item.docente_preinscrito.cedula,
                item.docente_preinscrito.departamento.nombre,
                item.docente_preinscrito.municipio.nombre,
                item.docente_preinscrito.radicado.numero,
                self.request.user.has_perm('permisos_sican.encuestas.respuestaspercepcioninicial.editar'),
                self.request.user.has_perm('permisos_sican.encuestas.respuestaspercepcioninicial.eliminar'),
            ])
        return json_data

class RadicadosRetomaList(BaseDatatableView):
    """
    0.id
    1.numero
    2.municipio
    3.departamento
    4.ubicacion
    5.institucion
    6.sede
    7.nombre completo
    8.dane
    9.permiso para editar
    10.permiso para eliminar
    """
    model = RadicadoRetoma
    columns = ['id','numero','municipio']

    order_columns = ['id','numero','municipio']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(numero__icontains=search) | Q(municipio__nombre__icontains=search) |\
                Q(municipio__departamento__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.numero,
                item.municipio.nombre,
                item.municipio.departamento.nombre,
                item.ubicacion,
                item.institucion,
                item.sede,
                item.nombre_completo,
                item.dane,
                self.request.user.has_perm('permisos_sican.acceso.radicadosretoma.editar'),
                self.request.user.has_perm('permisos_sican.acceso.radicadosretoma.eliminar'),
            ])
        return json_data

class RetomaList(BaseDatatableView):
    """
    0.id
    1.numero
    2.municipio
    3.departamento
    4.estado
    5.ubicacion
    6.institucion
    7.sede
    8.nombre completo
    9.dane
    10.permiso para editar
    11.permiso para eliminar
    """
    model = Retoma
    columns = ['id','id','id']

    order_columns = ['id','id','id']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(radicado__numero__icontains=search) | Q(radicado__municipio__nombre__icontains=search) |\
                Q(radicado__municipio__departamento__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def get_initial_queryset(self):
        return Retoma.objects.filter(lider = self.request.user)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.radicado.numero,
                item.radicado.municipio.nombre,
                item.radicado.municipio.departamento.nombre,
                item.estado,
                item.radicado.ubicacion,
                item.radicado.institucion,
                item.radicado.sede,
                item.radicado.nombre_completo,
                item.radicado.dane,
                self.request.user.has_perm('permisos_sican.acceso.retoma.editar'),
                self.request.user.has_perm('permisos_sican.acceso.retoma.eliminar'),
            ])
        return json_data

class MatricesDiplomadosList(BaseDatatableView):
    """
    0.id
    1.region
    2.radicado
    3.formador
    4.grupo
    5.apellidos
    6.nombres
    7.cedula
    8.correo
    9.telefono fijo
    10.telefono celular
    11.area
    12.grado
    13.genero
    14.estado
    15.permiso para editar
    16.permiso para eliminar
    """
    model = Beneficiario
    columns = ['region','radicado','formador','grupo','apellidos','nombres','cedula','correo']

    order_columns = ['region','radicado','formador','grupo','apellidos','nombres','cedula','correo']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(region__nombre__icontains=search) | Q(radicado__numero__icontains=search) |\
                Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) |\
                Q(apellidos__icontains=search) | Q(nombres__icontains=search) |\
                Q(cedula__icontains=search)

            qs = qs.filter(q)
        return qs

    def get_initial_queryset(self):
        diplomado = self.kwargs['diplomado']
        if diplomado == 'INNOVATIC':
            numero = 1
        elif diplomado == 'TECNOTIC':
            numero = 2
        elif diplomado == 'DIRECTIC':
            numero = 3
        elif diplomado == 'ESCUELATIC':
            numero = 4
        else:
            numero = 0
        return Beneficiario.objects.filter(diplomado__numero = numero)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.region.nombre,
                item.radicado.numero if item.radicado != None else 'N/A',
                item.formador.get_full_name(),
                item.grupo.get_full_name(),
                item.apellidos,
                item.nombres,
                item.cedula,
                item.correo,
                item.telefono_fijo,
                item.telefono_celular,
                item.area.nombre if item.area != None else 'N/A',
                item.grado.nombre if item.grado != None else 'N/A',
                item.genero,
                item.estado,
                self.request.user.has_perm('permisos_sican.acceso.retoma.editar'),
                self.request.user.has_perm('permisos_sican.acceso.retoma.eliminar'),
            ])
        return json_data


class BeneficiariosGruposList(BaseDatatableView):
    """
    """
    model = GruposBeneficiarios
    columns = ['nombre','numero','diplomado','descripcion']

    order_columns = ['nombre','nombre','numero','diplomado','descripcion']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search) | Q(numero__icontains=search) | Q(diplomado_grupo__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(usuario = self.request.user)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            contrato = ''
            if item.contrato != None:
                contrato = item.contrato.nombre
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                item.diplomado_grupo.nombre,
                item.descripcion,
                BeneficiarioVigencia.objects.filter(grupo__id = item.id).count(),
                contrato,
                self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.ver'),
            ])
        return json_data


class BeneficiariosCedulaListView(BaseDatatableView):
    """
    """
    model = Beneficiario
    columns = ['id','nombres','apellidos','cedula','region','diplomado','formador']
    order_columns = ['nombres','apellidos','cedula','region','diplomado','formador']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) |\
                Q(cedula__icontains=search) | Q(diplomado__nombre__icontains=search) |\
                Q(formador__nombres__icontains=search)

            qs = qs.filter(q)
        return qs


    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombres,
                item.apellidos,
                item.cedula,
                item.region.nombre,
                item.diplomado.nombre,
                item.formador.get_full_name()
            ])
        return json_data



class BeneficiariosVigencia2017CedulaListView(BaseDatatableView):
    """
    """
    model = BeneficiarioVigencia2017
    columns = ['id','nombres','apellidos','cedula','region','diplomado','formador']
    order_columns = ['nombres','apellidos','cedula','region','diplomado','formador']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) |\
                Q(cedula__icontains=search) | Q(grupo__diplomado__nombre__icontains=search) |\
                Q(grupo__contrato__formador__nombres__icontains=search)

            qs = qs.filter(q)
        return qs


    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombres,
                item.apellidos,
                item.cedula,
                item.region.nombre,
                item.grupo.diplomado.nombre,
                item.grupo.contrato.formador.get_full_name()
            ])
        return json_data



class BeneficiariosPleList(BaseDatatableView):
    """
    """
    model = Beneficiario
    columns = ['id','cedula','nombres','apellidos']
    order_columns = ['cedula','nombres','apellidos']
    max_display_length = 100

    def get_initial_queryset(self):
        return self.model.objects.filter(diplomado__id=1)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) |\
                Q(cedula__icontains=search) | Q(formador__nombres__icontains=search)

            qs = qs.filter(q)
        return qs


    def get_guia_url(self,id):
        evidencias = Evidencia.objects.filter(entregable__id=34).filter(beneficiarios_cargados__id=id)
        try:
            url = evidencias[0].archivo.url
        except:
            url = None
        return url


    def get_ple_url(self,id):
        evidencias = Evidencia.objects.filter(entregable__id=259).filter(beneficiarios_cargados__id=id).order_by('-id')
        try:
            url = evidencias[0].archivo.url
        except:
            url = None
        return url





    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.cedula,
                item.nombres,
                item.apellidos,
                item.formador.get_full_name(),
                item.region.nombre,
                self.get_guia_url(item.id),
                self.get_ple_url(item.id),
                item.link,
                item.estado_producto_final
            ])
        return json_data




class BeneficiariosCedulaProductosListView(BaseDatatableView):
    """
    """
    model = Entregable
    columns = ['id']
    order_columns = ['id']
    max_display_length = 100

    def get_initial_queryset(self):
        beneficiario = Beneficiario.objects.get(id=self.kwargs['id_beneficiario'])
        return Entregable.objects.filter(sesion__nivel__diplomado__id = beneficiario.diplomado.id)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) |\
                Q(cedula__icontains=search) | Q(diplomado__nombre__icontains=search) |\
                Q(formador__nombres__icontains=search)

            qs = qs.filter(q)
        return qs


    def prepare_results(self, qs):
        json_data = []

        beneficiario = Beneficiario.objects.get(id=self.kwargs['id_beneficiario'])
        evidencias = Evidencia.objects.filter(beneficiarios_cargados = beneficiario)

        for item in qs:
            evidencia = evidencias.filter(entregable__id = item.id)

            if evidencia.count() == 0:
                link = ''
            else:
                link = evidencia[0].get_archivo_url()

            json_data.append([
                item.id,
                item.sesion.nivel.diplomado.nombre,
                item.sesion.nivel.nombre,
                item.sesion.nombre,
                item.nombre,
                link
            ])
        return json_data




class BeneficiariosCedulaProductosVigencia2017ListView(BaseDatatableView):
    """
    """
    model = Entregable
    columns = ['id']
    order_columns = ['id']
    max_display_length = 100

    def get_initial_queryset(self):
        beneficiario = BeneficiarioVigencia2017.objects.get(id=self.kwargs['id_beneficiario'])
        return Entregable.objects.filter(sesion__nivel__diplomado__id = beneficiario.grupo.diplomado.id,escencial="Si")


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search) | Q(id__icontains=search)

            qs = qs.filter(q)
        return qs


    def prepare_results(self, qs):
        json_data = []

        beneficiario = BeneficiarioVigencia2017.objects.get(id=self.kwargs['id_beneficiario'])
        evidencias = EvidenciaVigencia2017.objects.filter(beneficiarios_cargados = beneficiario)

        for item in qs:
            evidencia = evidencias.filter(entregable__id = item.id).order_by('id')

            if evidencia.count() == 0:
                link = ''
            else:
                link = evidencia[0].get_archivo_url()

            json_data.append([
                item.id,
                item.sesion.nivel.diplomado.nombre,
                item.sesion.nivel.nombre,
                item.sesion.nombre,
                item.nombre,
                link
            ])
        return json_data




class BeneficiariosListView(BaseDatatableView):
    """
    """
    model = Beneficiario
    columns = ['region','radicado','formador','grupo','apellidos','nombres','cedula','correo']

    order_columns = ['region','radicado','formador','grupo','apellidos','nombres','cedula','correo']
    max_display_length = 100

    def get_initial_queryset(self):
        evidencias = Evidencia.objects.filter(entregable__id = self.kwargs['id_actividad']).values_list('beneficiarios_cargados__id',flat=True).distinct()
        evidencias = list(evidencias)
        if None in evidencias:
            evidencias.remove(None)
        return Beneficiario.objects.filter(id__in = evidencias)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:

            evidencia = Evidencia.objects.filter(entregable__id = self.kwargs['id_actividad'],beneficiarios_cargados__id = item.id)

            json_data.append([
                item.id,
                item.get_full_name(),
                item.cedula,
                evidencia[ evidencia.count() - 1 ].get_archivo_url()
            ])
        return json_data

class CertificadosEscuelaTic(BaseDatatableView):
    """
    0.id
    1.region
    2.radicado
    3.formador
    4.grupo
    5.apellidos
    6.nombres
    7.cedula
    8.correo
    9.telefono fijo
    10.telefono celular
    11.area
    12.grado
    13.genero
    14.estado
    15.permiso para editar
    16.permiso para eliminar
    """
    model = Beneficiario
    columns = ['id','region','formador','apellidos','nombres','cedula']

    order_columns = ['id','region','formador','apellidos','nombres','cedula']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(region__nombre__icontains=search) | Q(radicado__numero__icontains=search) |\
                Q(formador__nombres__icontains=search) | Q(formador__apellidos__icontains=search) |\
                Q(apellidos__icontains=search) | Q(nombres__icontains=search) |\
                Q(cedula__icontains=search)

            qs = qs.filter(q)
        return qs

    def get_initial_queryset(self):
        return Beneficiario.objects.filter(diplomado__numero = 4)

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.region.nombre,
                item.formador.get_full_name(),
                item.apellidos,
                item.nombres,
                item.cedula,
                item.get_diploma_url(),
                item.ip_descarga if item.ip_descarga != None else '',
                item.fecha_descarga if item.fecha_descarga != None else '',
            ])
        return json_data

class FormadoresGrupos(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.ruta
    6.cantiad de grupos
    7.permiso para editar
    """
    model = Formador
    columns = ['id','nombres','cargo','region','cedula']

    order_columns = ['nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            grupos = Grupos.objects.filter(formador = item,oculto = False)
            json_data.append([
                item.id,
                item.get_full_name(),
                item.get_cargo_string(),
                item.get_region_string(),
                item.cedula,
                item.codigo_ruta,
                grupos.count(),
                self.request.user.has_perm('permisos_sican.formacion.gruposformacion.editar'),
            ])
        return json_data

class FormadoresGruposLista(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.ruta
    6.permiso para editar
    """
    model = Grupos
    columns = ['id','nombre']

    order_columns = ['id','nombre']
    max_display_length = 100

    def get_initial_queryset(self):
        return Grupos.objects.filter(formador__id=self.kwargs['id_formador'],oculto=False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            json_data.append([
                item.id,
                item.get_full_name(),
                self.request.user.has_perm('permisos_sican.formacion.gruposformacion.editar'),
                self.request.user.has_perm('permisos_sican.formacion.gruposformacion.eliminar'),
            ])
        return json_data

class ContratosValorList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.cargo
    3.descripcion
    4.permiso para editar
    """
    model = Contratos
    columns = ['id','nombre','cargo','descripcion']

    order_columns = ['id','nombre','cargo','descripcion']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            valor_total = ValorEntregable.objects.filter(contrato = item).aggregate(Sum('valor'))
            json_data.append([
                item.id,
                item.nombre,
                item.cargo.nombre,
                item.descripcion,
                valor_total.get('valor__sum'),
            ])
        return json_data

class EntregablesValorList(BaseDatatableView):
    """
    0.id
    1.entregable
    2.valor
    """
    model = ValorEntregable
    columns = ['id']

    order_columns = ['id']
    max_display_length = 100

    def get_initial_queryset(self):
        return ValorEntregable.objects.filter(contrato__id=self.kwargs['id_contrato'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(entregable__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            json_data.append([
                item.id,
                item.entregable.nombre,
                item.entregable.sesion.nivel.diplomado.nombre,
                item.entregable.sesion.nivel.nombre,
                item.entregable.sesion.nombre,
                item.entregable.tipo,
                item.valor,
            ])
        return json_data

class FormadoresRevision(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.capacitación
    5.ruta
    6.valor
    7.permiso para editar
    """
    model = Formador
    columns = ['id','nombres','cargo','region','primera_capacitacion']

    order_columns = ['nombres','cargo']
    max_display_length = 100

    def get_initial_queryset(self):
        if self.request.user.has_perm('permisos_sican.formacion.revision.r1') and self.request.user.has_perm('permisos_sican.formacion.revision.r2'):
            return Formador.objects.filter(oculto = False)
        elif self.request.user.has_perm('permisos_sican.formacion.revision.r1'):
            return Formador.objects.filter(oculto = False,region__id=1)

        elif self.request.user.has_perm('permisos_sican.formacion.revision.r2'):
            return Formador.objects.filter(oculto = False,region__id=2)

        else:
            return Formador.objects.filter(oculto = False)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search) | Q(codigo_ruta__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:

                stack.append(item)

                valor = 0
                for revision in Revision.objects.filter(formador_revision = item):
                    for producto in revision.productos.all():
                        valor += producto.cantidad * producto.valor_entregable.valor
                json_data.append([
                    item.id,
                    item.nombres + " " + item.apellidos,
                    item.get_cargo_string(),
                    item.get_region_string(),
                    'Primera' if item.primera_capacitacion else 'Segunda',
                    item.codigo_ruta,
                    valor,
                    self.request.user.has_perm('permisos_sican.formacion.revision.editar')
                ])
        return json_data

class FormadoresRevisionFormador(BaseDatatableView):
    """
    0.id
    1.fecha
    2.descripcion
    3.valor
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Revision
    columns = ['id','fecha','descripcion']

    order_columns = ['fecha','descripcion']
    max_display_length = 100

    def get_initial_queryset(self):
        ids = []
        cargo = Cargo.objects.get(id=self.kwargs['id_cargo'])
        diplomado__id = 0

        if cargo.nombre == "Formador Tipo 1":
            diplomado__id = 1
        elif cargo.nombre == "Formador Tipo 2":
            diplomado__id = 2
        elif cargo.nombre == "Formador Tipo 3":
            diplomado__id = 3
        elif cargo.nombre == "Formador Tipo 4":
            diplomado__id = 4

        for revision in Revision.objects.filter(formador_revision__id=self.kwargs['id_formador']):
            diplomado = revision.productos.values_list('valor_entregable__entregable__sesion__nivel__diplomado__id',flat=True).distinct()
            if diplomado__id in diplomado:
                ids.append(revision.id)

        return Revision.objects.filter(formador_revision__id=self.kwargs['id_formador']).filter(id__in = ids)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            #q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
            #    Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            #qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:
            valor = 0
            for producto in item.productos.all():
                valor += producto.cantidad * producto.valor_entregable.valor
            json_data.append([
                item.id,
                item.fecha,
                item.descripcion,
                valor,
                self.request.user.has_perm('permisos_sican.formacion.revision.editar') if item.corte == None else False,
                self.request.user.has_perm('permisos_sican.formacion.revision.eliminar')
            ])
        return json_data


class FormadoresContratosFormador(BaseDatatableView):
    """
    0.id
    1.fecha
    2.descripcion
    3.valor
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Cargo
    columns = ['id','nombre']

    order_columns = ['id','nombre']
    max_display_length = 100

    def get_initial_queryset(self):
        formador = Formador.objects.get(id=self.kwargs['id_formador'])
        cargos = formador.cargo.all().values_list('id',flat=True)
        return Cargo.objects.filter(id__in = cargos)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            #q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
            #    Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            #qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        formador = Formador.objects.get(id=self.kwargs['id_formador'])

        for item in qs:

            valor = 0

            diplomado = None

            if item.nombre == "Formador Tipo 1":
                diplomado = Diplomado.objects.get(id=1)
            elif item.nombre == "Formador Tipo 2":
                diplomado = Diplomado.objects.get(id=2)
            elif item.nombre == "Formador Tipo 3":
                diplomado = Diplomado.objects.get(id=3)
            elif item.nombre == "Formador Tipo 4":
                diplomado = Diplomado.objects.get(id=4)

            revisiones = Revision.objects.filter(formador_revision = formador)

            for revision in revisiones:
                for producto in revision.productos.all():
                    if producto.valor_entregable.entregable.sesion.nivel.diplomado == diplomado:
                        valor += producto.cantidad * producto.valor_entregable.valor

            json_data.append([
                item.id,
                item.nombre,
                valor,
                self.request.user.has_perm('permisos_sican.formacion.revision.editar'),
                self.request.user.has_perm('permisos_sican.formacion.revision.eliminar')
            ])
        return json_data


class CortesList(BaseDatatableView):
    """
    0.id
    1.fecha
    2.descripcion
    3.valor
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Cortes
    columns = ['id','fecha','descripcion']

    order_columns = ['fecha']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            #q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
            #    Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            #qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:
            json_data.append([
                item.id,
                item.fecha,
                item.descripcion,
                item.get_archivo_url()
            ])
        return json_data

class RequerimientosContratacion(BaseDatatableView):
    """
    0.id
    1.encargado
    2.codigo_ruta
    3.departamento
    4.municipios
    5.estado
    6.permiso para editar
    """
    model = RequerimientoPersonal
    columns = ['id','encargado','codigo_ruta','departamento']

    order_columns = ['id','encargado','codigo_ruta','departamento']
    max_display_length = 100

    def get_initial_queryset(self):
        grupos = self.request.user.groups.values_list('name',flat=True)
        if 'Coordinadores operativos' in grupos:
            return RequerimientoPersonal.objects.all()
        else:
            q = Q(solicitante = self.request.user) | Q(encargado = self.request.user)
            return RequerimientoPersonal.objects.filter(q)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search == 'Remitido a RH':
            q = Q(remitido_respuesta = False) & Q(remitido_contratacion = False) & Q(contratar = False) & Q(desierto = False) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Listo para capacitar':
            q = Q(remitido_respuesta = True) & Q(remitido_contratacion = False) & Q(contratar = False) & Q(desierto = False) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Proceder a contrato':
            q = Q(remitido_respuesta = True) & Q(remitido_contratacion = True) & Q(contratar = True) & Q(desierto = False) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Aspirante deserta':
            q = Q(remitido_respuesta = True) & Q(remitido_contratacion = True) & Q(contratar = False) & Q(desierto = True) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Contrato enviado':
            q = Q(contrato_enviado = True) & Q(contratado = False)
            qs = qs.filter(q)
        elif search == 'Contratado':
            q = Q(contratado = True)
            qs = qs.filter(q)
        else:
            q = Q(solicitante__first_name__icontains = search) | Q(encargado__first_name__icontains = search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            if item.remitido_respuesta == False and item.remitido_contratacion == False and item.contratar == False and item.desierto == False and item.contratado == False and item.contrato_enviado == False:
                estado = 'Remitido a RH'
                editar = False

            elif item.remitido_respuesta == True and item.remitido_contratacion == False and item.contratar == False and item.desierto == False and item.contratado == False and item.contrato_enviado == False:
                estado = 'Listo para capacitar'
                editar = True

            elif item.remitido_respuesta == True and item.remitido_contratacion == True and item.contratar == True and item.desierto == False and item.contratado == False and item.contrato_enviado == False:
                estado = 'Proceder a contrato'
                editar = False

            elif item.remitido_respuesta == True and item.remitido_contratacion == True and item.contratar == False and item.desierto == True and item.contratado == False and item.contrato_enviado == False:
                estado = 'Aspirante deserta'
                editar = False

            elif item.contratado == False and item.contrato_enviado == True:
                estado = 'Contrato enviado'
                editar = False

            elif item.contratado == True:
                estado = 'Contratado'
                editar = False


            json_data.append([
                item.id,
                item.encargado.first_name + ' ' + item.encargado.last_name,
                item.codigo_ruta,
                item.departamento.nombre,
                item.get_municipios_string(),
                estado,
                editar
            ])
        return json_data

class RequerimientosContratacionRespuesta(BaseDatatableView):
    """
    0.id
    1.encargado
    2.codigo_ruta
    3.departamento
    4.municipios
    5.estado
    6.permiso para editar
    """
    model = RequerimientoPersonal
    columns = ['id','encargado','codigo_ruta','departamento']

    order_columns = ['id','encargado','codigo_ruta','departamento']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search == 'Remitido a RH':
            q = Q(remitido_respuesta = False) & Q(remitido_contratacion = False) & Q(contratar = False) & Q(desierto = False) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Listo para capacitar':
            q = Q(remitido_respuesta = True) & Q(remitido_contratacion = False) & Q(contratar = False) & Q(desierto = False) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Proceder a contrato':
            q = Q(remitido_respuesta = True) & Q(remitido_contratacion = True) & Q(contratar = True) & Q(desierto = False) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Aspirante deserta':
            q = Q(remitido_respuesta = True) & Q(remitido_contratacion = True) & Q(contratar = False) & Q(desierto = True) & Q(contratado = False) & Q(contrato_enviado = False)
            qs = qs.filter(q)
        elif search == 'Contrato enviado':
            q = Q(contrato_enviado = True) & Q(contratado = False)
            qs = qs.filter(q)
        elif search == 'Contratado':
            q = Q(contratado = True)
            qs = qs.filter(q)
        else:
            q = Q(solicitante__first_name__icontains = search) | Q(encargado__first_name__icontains = search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            if item.remitido_respuesta == False and item.remitido_contratacion == False and item.contratar == False and item.desierto == False and item.contratado == False and item.contrato_enviado == False:
                estado = 'Remitido a RH'
                editar = True

            elif item.remitido_respuesta == True and item.remitido_contratacion == False and item.contratar == False and item.desierto == False and item.contratado == False and item.contrato_enviado == False:
                estado = 'Listo para capacitar'
                editar = True

            elif item.remitido_respuesta == True and item.remitido_contratacion == True and item.contratar == True and item.desierto == False and item.contratado == False and item.contrato_enviado == False:
                estado = 'Proceder a contrato'
                editar = True

            elif item.remitido_respuesta == True and item.remitido_contratacion == True and item.contratar == False and item.desierto == True and item.contratado == False and item.contrato_enviado == False:
                estado = 'Aspirante deserta'
                editar = True

            elif item.contratado == False and item.contrato_enviado == True:
                estado = 'Contrato enviado'
                editar = True

            elif item.contratado == True:
                estado = 'Contratado'
                editar = True


            json_data.append([
                item.id,
                item.encargado.first_name + ' ' + item.encargado.last_name,
                item.codigo_ruta,
                item.departamento.nombre,
                item.get_municipios_string(),
                estado,
                editar
            ])
        return json_data

class CargaMasivaMatrices(BaseDatatableView):
    """
    0.id
    1.fecha
    2.archivo
    3.resultado
    4.estado
    """
    model = CargaMasiva
    columns = ['id','fecha','archivo','resultado','estado']

    order_columns = ['id','fecha','archivo','resultado','estado']
    max_display_length = 100

    def get_initial_queryset(self):
        return CargaMasiva.objects.filter(usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        search = unicode(search).capitalize()
        if search:
            q = Q(id__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.fecha,
                item.get_archivo_url(),
                item.get_resultado_url(),
                item.estado
            ])
        return json_data

class FormadoresListEvidencias(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.fecha_contratacion
    9.fecha_terminacion
    10.banco
    11.tipo_cuenta
    12.numero_cuenta
    13.eps
    14.pension
    15.arl
    16.grupos
    17.beneficiarios
    """
    model = Formador
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'fecha_contratacion','fecha_terminacion','banco','tipo_cuenta','numero_cuenta','eps',
               'pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        qs = Formador.objects.filter(cargo__nombre = 'Formador Tipo ' + self.kwargs['id_diplomado'])
        return qs

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:
            if item not in stack:
                stack.append(item)
                region_str = ''
                for region in item.region.values_list('numero',flat=True):
                    region_str = region_str + str(region) + ','
                region_str = region_str[:-1]

                if item.banco != None:
                    banco = item.banco.nombre
                else:
                    banco = ''

                grupos = Grupos.objects.filter(formador = item).count()
                beneficiarios = Beneficiario.objects.filter(formador = item,diplomado__id=self.kwargs['id_diplomado']).count()

                json_data.append([
                    item.id,
                    item.nombres + " " + item.apellidos,
                    'Formador Tipo ' + self.kwargs['id_diplomado'],
                    region_str,
                    item.cedula,
                    item.correo_personal,
                    item.celular_personal,
                    item.profesion,
                    item.fecha_contratacion,
                    item.fecha_terminacion,
                    banco,
                    item.tipo_cuenta,
                    item.numero_cuenta,
                    item.eps,
                    item.pension,
                    item.arl,
                    grupos,
                    beneficiarios
                ])
        return json_data

class DiplomadosEvidenciasList(BaseDatatableView):
    """
    0.id
    1.nombre
    2.numero
    3.cantidad formadores
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Diplomado
    columns = ['id','nombre','numero']

    order_columns = ['nombre','numero']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = search.upper()
            q = Q(nombre__icontains=search) | Q(numero__icontains=search)

            qs = qs.filter(q)

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            cantidad = Formador.objects.filter(cargo__nombre = 'Formador Tipo ' + str(item.id)).count()
            json_data.append([
                item.id,
                item.nombre,
                item.numero,
                cantidad,
                self.request.user.has_perm('permisos_sican.evidencias.general.editar'),
                self.request.user.has_perm('permisos_sican.evidencias.general.eliminar'),
            ])
        return json_data

class NivelesListEvidencias(BaseDatatableView):
    """
    0.id
    1.nombre
    2.sesiones
    3.entregables
    4.escenciales
    """
    model = Nivel
    columns = ['id','nombre']

    order_columns = ['nombre']
    max_display_length = 100

    def get_initial_queryset(self):
        return Nivel.objects.filter(diplomado__id = self.kwargs['id_diplomado'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            sesiones = Sesion.objects.filter(nivel = item).count()
            entregables = Entregable.objects.filter(sesion__nivel=item).count()
            escenciales = Entregable.objects.filter(sesion__nivel=item).filter(escencial = 'Si').count()
            json_data.append([
                item.id,
                item.nombre,
                sesiones,
                entregables,
                escenciales
            ])
        return json_data

class SesionesListEvidencias(BaseDatatableView):
    """
    0.id
    1.nombre
    """
    model = Sesion
    columns = ['id','nombre']

    order_columns = ['nombre']
    max_display_length = 100

    def get_initial_queryset(self):
        return Sesion.objects.filter(nivel__id = self.kwargs['id_nivel'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize())
            qs = qs.filter(q)
        return qs

class EntregablesListEvidencias(BaseDatatableView):
    """
    0.id
    1.nombre
    2.tipo
    3.escencial
    """
    model = Entregable
    columns = ['id','nombre','tipo','escencial']

    order_columns = ['id','nombre','tipo','escencial']
    max_display_length = 100

    def get_initial_queryset(self):
        return Entregable.objects.filter(sesion__id = self.kwargs['id_sesion'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize())
            qs = qs.filter(q)
        return qs

class SoportesListEvidencias(BaseDatatableView):
    """
    0.id
    1.beneficiarios
    2.aprobados
    3.archivo
    4.editar
    5.eliminar
    """
    model = Evidencia
    columns = ['id']

    order_columns = ['id']
    max_display_length = 100

    def get_initial_queryset(self):
        return Evidencia.objects.filter(formador__id = self.kwargs['id_formador'],entregable__id = self.kwargs['id_entregable'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            red = Red.objects.filter(evidencias__id = item.id).count()
            baneficiarios_cargados = []
            baneficiarios_validados = []
            baneficiarios_rechazados = []

            for beneficiario in item.beneficiarios_cargados.all():
                if beneficiario != None:
                    baneficiarios_cargados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.get_grupo()])

            for beneficiario in item.beneficiarios_validados.all():
                if beneficiario != None:
                    baneficiarios_validados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.get_grupo()])

            for beneficiario in item.beneficiarios_rechazados.all():
                if beneficiario != None:
                    baneficiarios_rechazados.append([beneficiario.beneficiario_rechazo.get_full_name(),beneficiario.beneficiario_rechazo.cedula,beneficiario.beneficiario_rechazo.get_grupo(),beneficiario.observacion])


            json_data.append([
                item.id,
                item.get_beneficiarios_cantidad(),
                item.get_validados_cantidad(),
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.evidencias.general.editar') if red == 0 else False,
                self.request.user.has_perm('permisos_sican.evidencias.general.eliminar') if red == 0 else False,
                baneficiarios_cargados,
                baneficiarios_validados,
                baneficiarios_rechazados
            ])
        return json_data

class DelegacionRequerimientos(BaseDatatableView):
    """

    """
    model = Requerimiento
    columns = ['id','nombre','recepcion_solicitud','entidad_remitente','funcionario_remitente','tiempo_respuesta']

    order_columns = ['id','nombre','recepcion_solicitud','entidad_remitente','funcionario_remitente','tiempo_respuesta']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains=search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.recepcion_solicitud,
                item.get_dias_mora(),
                item.get_region_string(),
                item.estado,

                item.entidad_remitente,
                item.funcionario_remitente,
                item.get_archivo_solicitud_url(),
                item.descripcion,

                item.tiempo_respuesta,
                item.get_encargados_string(),
                item.medio_entrega,

                item.fecha_respuesta,
                item.observaciones,
                item.get_archivo_respuesta_url(),

                self.request.user.has_perm('permisos_sican.requerimientos.proyecto.editar'),
                self.request.user.has_perm('permisos_sican.requerimientos.proyecto.eliminar')
            ])
        return json_data

class EvidenciasCodigos(BaseDatatableView):
    """
    0.id
    1.red
    2.fecha
    3.actualizacion
    4.usuario
    5.archivo
    6.entregable
    7.beneficiarios cargados
    8.beneficiarios validados
    9.formador
    """
    model = Evidencia
    columns = ['id']

    order_columns = ['id','id','id','id']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            red = ''

            if item.red_id != None:
                red = 'RED-' + str(item.red_id)


            baneficiarios_cargados = []
            baneficiarios_validados = []
            baneficiarios_rechazados = []

            for beneficiario in item.beneficiarios_cargados.all():
                if beneficiario != None:
                    baneficiarios_cargados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.get_grupo()])

            for beneficiario in item.beneficiarios_validados.all():
                if beneficiario != None:
                    baneficiarios_validados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.get_grupo()])

            for beneficiario in item.beneficiarios_rechazados.all():
                if beneficiario != None:
                    baneficiarios_rechazados.append([beneficiario.beneficiario_rechazo.get_full_name(),beneficiario.beneficiario_rechazo.cedula,beneficiario.beneficiario_rechazo.get_grupo(),beneficiario.observacion])


            json_data.append([
                item.id,
                red,
                item.get_beneficiarios_cantidad(),
                item.get_validados_cantidad(),
                item.get_archivo_url(),
                item.entregable.sesion.nivel.diplomado.nombre,
                item.entregable.sesion.nivel.nombre,
                item.entregable.sesion.nombre,
                item.entregable.id,

                localtime(item.fecha).strftime('%d/%m/%Y %I:%M:%S %p'),
                localtime(item.updated).strftime('%d/%m/%Y %I:%M:%S %p'),
                item.usuario.get_full_name(),
                item.entregable.nombre,
                item.formador.get_full_name(),
                baneficiarios_cargados,
                baneficiarios_validados,
                baneficiarios_rechazados
            ])
        return json_data



class EvidenciasCodigosVigencia2017(BaseDatatableView):
    """
    0.id
    1.red
    2.fecha
    3.actualizacion
    4.usuario
    5.archivo
    6.entregable
    7.beneficiarios cargados
    8.beneficiarios validados
    9.formador
    """
    model = EvidenciaVigencia2017
    columns = ['id']

    order_columns = ['id','id','id','id']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            red = ''

            if item.red_id != None:
                red = 'RED-' + str(item.red_id)


            baneficiarios_cargados = []
            baneficiarios_validados = []
            baneficiarios_rechazados = []

            for beneficiario in item.beneficiarios_cargados.all():
                if beneficiario != None:
                    baneficiarios_cargados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.grupo.get_nombre_grupo()])

            for beneficiario in item.beneficiarios_validados.all():
                if beneficiario != None:
                    baneficiarios_validados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.grupo.get_nombre_grupo()])

            for beneficiario in item.beneficiarios_rechazados.all():
                if beneficiario != None:
                    baneficiarios_rechazados.append([beneficiario.beneficiario_rechazo.get_full_name(),beneficiario.beneficiario_rechazo.cedula,beneficiario.beneficiario_rechazo.grupo.get_nombre_grupo(),beneficiario.observacion])


            json_data.append([
                item.id,
                red,
                item.get_beneficiarios_cantidad(),
                item.get_validados_cantidad(),
                item.get_archivo_url(),
                item.entregable.sesion.nivel.diplomado.nombre,
                item.entregable.sesion.nivel.nombre,
                item.entregable.sesion.nombre,
                item.entregable.id,

                localtime(item.fecha).strftime('%d/%m/%Y %I:%M:%S %p'),
                localtime(item.updated).strftime('%d/%m/%Y %I:%M:%S %p'),
                item.usuario.get_full_name(),
                item.entregable.nombre,
                item.contrato.formador.get_full_name(),
                baneficiarios_cargados,
                baneficiarios_validados,
                baneficiarios_rechazados
            ])
        return json_data


class EvidenciasSubsanacionCodigos(BaseDatatableView):
    """
    0.id
    1.red
    2.fecha
    3.actualizacion
    4.usuario
    5.archivo
    6.entregable
    7.beneficiarios cargados
    8.beneficiarios validados
    9.formador
    """
    model = Evidencia
    columns = ['id']

    order_columns = ['id','id','id','id']
    max_display_length = 100


    def get_initial_queryset(self):
        red = Red.objects.get(id=self.kwargs['id_red'])
        ids = Evidencia.objects.filter(red_id=red.id).exclude(beneficiarios_rechazados = None).values_list('id',flat=True)
        return Evidencia.objects.filter(id__in = ids)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            try:
                red = 'RED-' + str(Red.objects.get(evidencias__id = item.id).id)
            except:
                red = None


            baneficiarios_cargados = []
            baneficiarios_validados = []
            baneficiarios_rechazados = []

            for beneficiario in item.beneficiarios_cargados.all():
                if beneficiario != None:
                    baneficiarios_cargados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.get_grupo()])

            for beneficiario in item.beneficiarios_validados.all():
                if beneficiario != None:
                    baneficiarios_validados.append([beneficiario.get_full_name(),beneficiario.cedula,beneficiario.get_grupo()])

            for beneficiario in item.beneficiarios_rechazados.all():
                if beneficiario != None:
                    baneficiarios_rechazados.append([beneficiario.beneficiario_rechazo.get_full_name(),beneficiario.beneficiario_rechazo.cedula,beneficiario.beneficiario_rechazo.get_grupo(),beneficiario.observacion])


            subsanadas = Subsanacion.objects.filter(red__id = self.kwargs['id_red'],evidencia_origen__id = item.id).aggregate(Sum('evidencia_subsanada__cantidad_cargados'))['evidencia_subsanada__cantidad_cargados__sum']

            json_data.append([
                item.id,
                item.get_rechazados_cantidad(),
                item.get_beneficiarios_cantidad(),
                item.get_validados_cantidad(),
                item.get_archivo_url(),
                item.entregable.sesion.nivel.diplomado.nombre,
                item.entregable.sesion.nivel.nombre,
                item.entregable.sesion.nombre,
                item.entregable.id,

                localtime(item.fecha).strftime('%d/%m/%Y %I:%M:%S %p'),
                localtime(item.updated).strftime('%d/%m/%Y %I:%M:%S %p'),
                item.usuario.get_full_name(),
                item.entregable.nombre,
                item.formador.get_full_name(),
                baneficiarios_cargados,
                baneficiarios_validados,
                baneficiarios_rechazados,
                subsanadas if subsanadas != None else 0
            ])
        return json_data



class EvidenciasSubsanacionCodigosSubsanacion(BaseDatatableView):
    """

    """
    model = Subsanacion
    columns = ['id']

    order_columns = ['id','id','id','id']
    max_display_length = 100


    def get_initial_queryset(self):
        return Subsanacion.objects.filter(evidencia_origen__id = self.kwargs['id_evidencia'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            json_data.append([
                item.id,
                item.usuario.get_full_name_string(),
                localtime(item.date).strftime('%d/%m/%Y %I:%M:%S %p'),
                item.evidencia_subsanada.cantidad_cargados,
                item.get_archivo_url(),
            ])
        return json_data




class RedList(BaseDatatableView):
    """
    """
    model = Red
    columns = ['id','diplomado','region','fecha']

    order_columns = ['id','diplomado','region','fecha']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            json_data.append([
                item.id,
                item.diplomado.nombre,
                item.region.nombre,
                localtime(item.fecha).strftime('%d/%m/%Y %I:%M:%S %p'),
                Evidencia.objects.filter(red_id = item.id).count(),
                'Si' if item.retroalimentacion else 'No',
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.evidencias.red.editar'),
            ])
        return json_data



class RedListVigencia2017(BaseDatatableView):
    """
    """
    model = RedVigencia2017
    columns = ['id','diplomado','region','fecha']

    order_columns = ['id','diplomado','region','fecha']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            json_data.append([
                item.id,
                item.diplomado.nombre,
                item.region.nombre,
                localtime(item.fecha).strftime('%d/%m/%Y %I:%M:%S %p'),
                Evidencia.objects.filter(red_id = item.id).count(),
                'Si' if item.retroalimentacion else 'No',
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.evidencias.red.editar'),
            ])
        return json_data



class RedSubsanacionList(BaseDatatableView):
    """
    """
    model = Red
    columns = ['id','diplomado','region','fecha']

    order_columns = ['id','diplomado','region','fecha']
    max_display_length = 100


    def get_initial_queryset(self):
        return Red.objects.filter(retroalimentacion = True)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            cargados = list(Evidencia.objects.filter(red_id = item.id).values_list('beneficiarios_cargados__id',flat=True))
            validados = list(Evidencia.objects.filter(red_id = item.id).values_list('beneficiarios_validados__id',flat=True))
            rechazados = list(Evidencia.objects.filter(red_id = item.id).values_list('beneficiarios_rechazados__id',flat=True))
            subsanadas = Subsanacion.objects.filter(red__id = item.id).aggregate(Sum('evidencia_subsanada__cantidad_cargados'))['evidencia_subsanada__cantidad_cargados__sum']

            while None in cargados:
                cargados.remove(None)
            while None in validados:
                validados.remove(None)
            while None in rechazados:
                rechazados.remove(None)


            json_data.append([
                item.id,
                item.diplomado.nombre,
                item.region.nombre,
                item.evidencias.exclude(beneficiarios_cargados = None).count(),
                len(cargados),
                len(validados),
                len(rechazados),
                len(cargados)-len(validados)-len(rechazados),
                subsanadas if subsanadas != None else 0,
                item.get_archivo_url(),
                self.request.user.has_perm('permisos_sican.evidencias.red.editar'),
            ])
        return json_data


class CohortesFormadorList(BaseDatatableView):
    """
    """
    model = CohortesFormadores
    columns = ['id','nombre','fecha','archivo','resultado']

    order_columns = ['id','nombre']
    max_display_length = 100




    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)

        if search:
            q = Q(nombre__icontains = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:

            json_data.append([
                item.id,
                item.nombre,
                item.fecha,
                item.get_archivo_url(),
                item.get_resultado_url(),
                item.get_contratos_url(),
                self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.ver'),
            ])
        return json_data


class CargaMasivaEvidenciasList(BaseDatatableView):
    """
    """
    model = CargaMasivaEvidencias
    columns = ['id','fecha','usuario','excel','zip','resultado']

    order_columns = ['id','fecha','usuario','excel','zip','resultado']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(id__exact = search.capitalize())
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            json_data.append([
                'MASE-' + str(item.id),
                localtime(item.fecha).strftime('%d/%m/%Y %I:%M:%S %p'),
                item.usuario.get_full_name_string(),
                item.get_excel_url(),
                item.get_zip_url(),
                item.get_resultado_url()
            ])
        return json_data

class RendimientoAuxiliaresList(BaseDatatableView):
    """
    """
    model = User
    columns = ['id','first_name','email']

    order_columns = ['id','first_name','email']
    max_display_length = 100

    def get_initial_queryset(self):
        return User.objects.filter(id__in = Evidencia.objects.all().values_list('usuario__id',flat=True).distinct())


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(first_name__icontains = search.capitalize()) | Q(email__icontains = search.capitalize())
            qs = qs.filter(q)
        return qs


    def prepare_results(self, qs):
        json_data = []
        now = datetime.datetime.now()
        for item in qs:
            json_data.append([
                item.id,
                item.get_full_name_string(),
                item.email,
                Evidencia.objects.filter(usuario = item).count(),
                Evidencia.objects.filter(usuario = item,updated__year = str(now.year),updated__month = str(now.month),updated__day = str(now.day)).count()
            ])
        return json_data


#--------------------------------------------------RH-------------------------------------------------------------------

class AdministrativosRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.correo_corporativo
    9.celular_corporativo
    10.fecha_contratacion
    11.fecha_terminacion
    12.banco
    13.tipo_cuenta
    14.numero_cuenta
    15.eps
    16.pension
    17.arl
    18.permiso para editar
    19.permiso para eliminar
    20.permiso para ver soportes
    """
    model = Administrativo
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'correo_corporativo','celular_corporativo','fecha_contratacion','fecha_terminacion',
               'banco','tipo_cuenta','numero_cuenta','eps','pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Administrativo.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            region_str = ''
            for region in item.region.values_list('numero',flat=True):
                region_str = region_str + str(region) + ','
            region_str = region_str[:-1]

            if item.banco != None:
                banco = item.banco.nombre
            else:
                banco = ''

            json_data.append([
                item.id,
                item.nombres + " " + item.apellidos,
                item.cargo.nombre,
                region_str,
                item.cedula,
                item.correo_personal,
                item.celular_personal,
                item.profesion,
                item.correo_corporativo,
                item.celular_corporativo,
                item.fecha_contratacion,
                item.fecha_terminacion,
                banco,
                item.tipo_cuenta,
                item.numero_cuenta,
                item.eps,
                item.pension,
                item.arl,
                self.request.user.has_perm('permisos_sican.rh.rh_administrativos.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_administrativos.eliminar'),
                self.request.user.has_perm('permisos_sican.rh.rh_administrativos_soportes.ver'),
            ])
        return json_data

class AdministrativosRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.archivo (url o string vacio)
    5.creacion
    6.permiso para editar
    7.permiso para eliminar
    """
    model = Soporte
    columns = ['id','tipo','fecha','descripcion','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion']
    max_display_length = 100

    def get_initial_queryset(self):
        return Soporte.objects.filter(oculto = False,administrativo__id=self.kwargs['id_administrativo'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.tipo.nombre,
                item.fecha,
                item.tipo.descripcion,
                item.get_archivo_url(),
                item.creacion,
                self.request.user.has_perm('permisos_sican.rh.rh_administrativos_soportes.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_administrativos_soportes.eliminar'),
            ])
        return json_data


class LideresRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.fecha_contratacion
    9.fecha_terminacion
    10.banco
    11.tipo_cuenta
    12.numero_cuenta
    13.eps
    14.pension
    15.arl
    16.permiso para editar
    17.permiso para eliminar
    18.permiso para ver soportes
    """
    model = Lideres
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'fecha_contratacion','fecha_terminacion','banco','tipo_cuenta','numero_cuenta','eps',
               'pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Lideres.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            if item.banco != None:
                banco = item.banco.nombre
            else:
                banco = ''

            json_data.append([
                item.id,
                item.nombres + " " + item.apellidos,
                item.cargo.nombre,
                item.region.nombre,
                item.cedula,
                item.correo_personal,
                item.celular_personal,
                item.profesion,
                item.fecha_contratacion,
                item.fecha_terminacion,
                banco,
                item.tipo_cuenta,
                item.numero_cuenta,
                item.eps,
                item.pension,
                item.arl,
                self.request.user.has_perm('permisos_sican.rh.rh_lideres.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_lideres.eliminar'),
                self.request.user.has_perm('permisos_sican.rh.rh_lideres_soportes.ver'),
            ])
        return json_data

class LideresRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.contrato
    5.archivo (url o string vacio)
    6.creacion
    7.permiso para editar
    8.permiso para eliminar
    """
    model = SoporteLider
    columns = ['id','tipo','fecha','descripcion','contrato','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion','contrato']
    max_display_length = 100

    def get_initial_queryset(self):
        return SoporteLider.objects.filter(oculto = False,lider__id=self.kwargs['id_lider'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.tipo.nombre,
                item.fecha,
                item.tipo.descripcion,
                item.contrato.nombre if item.contrato != None else '',
                item.get_archivo_url(),
                item.creacion,
                self.request.user.has_perm('permisos_sican.rh.rh_lideres_soportes.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_lideres_soportes.eliminar'),
            ])
        return json_data


class NegociadoresRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.fecha_contratacion
    9.fecha_terminacion
    10.banco
    11.tipo_cuenta
    12.numero_cuenta
    13.eps
    14.pension
    15.arl
    16.permiso para editar
    17.permiso para eliminar
    18.permiso para ver soportes
    """
    model = Negociador
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'fecha_contratacion','fecha_terminacion','banco','tipo_cuenta','numero_cuenta','eps',
               'pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Negociador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []


        for item in qs:

            if item.banco != None:
                banco = item.banco.nombre
            else:
                banco = ''

            json_data.append([
                item.id,
                item.nombres + " " + item.apellidos,
                item.cargo.nombre,
                item.region.nombre,
                item.cedula,
                item.correo_personal,
                item.celular_personal,
                item.profesion,
                item.fecha_contratacion,
                item.fecha_terminacion,
                banco,
                item.tipo_cuenta,
                item.numero_cuenta,
                item.eps,
                item.pension,
                item.arl,
                self.request.user.has_perm('permisos_sican.rh.rh_negociadores.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_negociadores.eliminar'),
                self.request.user.has_perm('permisos_sican.rh.rh_negociadores.ver'),
            ])
        return json_data

class NegociadoresRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.contrato
    5.archivo (url o string vacio)
    6.creacion
    7.permiso para editar
    8.permiso para eliminar
    """
    model = SoporteNegociador
    columns = ['id','tipo','fecha','descripcion','contrato','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion','contrato']
    max_display_length = 100

    def get_initial_queryset(self):
        return SoporteNegociador.objects.filter(oculto = False,negociador__id=self.kwargs['id_negociador'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.tipo.nombre,
                item.fecha,
                item.tipo.descripcion,
                item.contrato.nombre if item.contrato != None else '',
                item.get_archivo_url(),
                item.creacion,
                self.request.user.has_perm('permisos_sican.rh.rh_negociadores_soportes.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_negociadores_soportes.eliminar'),
            ])
        return json_data


class FormadoresRh(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cargo
    3.region
    4.cedula
    5.correo_personal
    6.celular_personal
    7.profesion
    8.fecha_contratacion
    9.fecha_terminacion
    10.banco
    11.tipo_cuenta
    12.numero_cuenta
    13.eps
    14.pension
    15.arl
    16.permiso para editar
    17.permiso para eliminar
    18.permiso para ver soportes
    """
    model = Formador
    columns = ['id','nombres','cargo','region','cedula','correo_personal','celular_personal','profesion',
               'fecha_contratacion','fecha_terminacion','banco','tipo_cuenta','numero_cuenta','eps',
               'pension','arl']

    order_columns = ['','nombres','cargo','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cargo__nombre__icontains=search) | \
                Q(region__numero__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                region_str = ''
                for region in item.region.values_list('numero',flat=True):
                    region_str = region_str + str(region) + ','
                region_str = region_str[:-1]

                if item.banco != None:
                    banco = item.banco.nombre
                else:
                    banco = ''

                json_data.append([
                    item.id,
                    item.nombres + " " + item.apellidos,
                    item.get_cargo_string(),
                    region_str,
                    item.cedula,
                    item.correo_personal,
                    item.celular_personal,
                    item.profesion,
                    item.fecha_contratacion,
                    item.fecha_terminacion,
                    banco,
                    item.tipo_cuenta,
                    item.numero_cuenta,
                    item.eps,
                    item.pension,
                    item.arl,
                    self.request.user.has_perm('permisos_sican.rh.rh_formadores.editar'),
                    self.request.user.has_perm('permisos_sican.rh.rh_formadores.eliminar'),
                    self.request.user.has_perm('permisos_sican.rh.rh_formadores_soportes.ver'),
                ])
        return json_data

class FormadoresRhSoportes(BaseDatatableView):
    """
    0.id
    1.tipo
    2.fecha
    3.descripcion
    4.contrato
    5.archivo (url o string vacio)
    6.creacion
    7.permiso para editar
    8.permiso para eliminar
    """
    model = SoporteFormador
    columns = ['id','tipo','fecha','descripcion','contrato','get_archivo_url','creacion']

    order_columns = ['id','tipo','fecha','descripcion','contrato']
    max_display_length = 100

    def get_initial_queryset(self):
        return SoporteFormador.objects.filter(oculto = False,formador__id=self.kwargs['id_formador'])


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(tipo__nombre__icontains=search) | Q(tipo__descripcion__icontains=search) | Q(fecha__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.tipo.nombre,
                item.fecha,
                item.tipo.descripcion,
                item.contrato.nombre if item.contrato != None else '',
                item.get_archivo_url(),
                item.creacion,
                self.request.user.has_perm('permisos_sican.rh.rh_formadores_soportes.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_formadores_soportes.eliminar'),
            ])
        return json_data



class CargosRh(BaseDatatableView):
    """
    0.id
    1.nombre
    2.manual (retorna la url o string vacio)
    3.descripcion
    4.permiso para editar
    5.permiso para eliminar
    """
    model = Cargo
    columns = ['id','nombre','manual','descripcion']

    order_columns = ['','nombre','']
    max_display_length = 100

    def get_initial_queryset(self):
        return Cargo.objects.filter(oculto = False)


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            try:
                url = item.manual.url
            except:
                url = ""

            json_data.append([
                item.id,
                item.nombre,
                url,
                item.descripcion,
                self.request.user.has_perm('permisos_sican.rh.rh_cargos.editar'),
                self.request.user.has_perm('permisos_sican.rh.rh_cargos.eliminar'),
            ])
        return json_data

class TipoSoporteRh(BaseDatatableView):
    """
    0.id
    1.nombre
    2.descripcion
    3.permiso para editar
    4.permiso para eliminar
    """
    model = TipoSoporte
    columns = ['id','nombre','descripcion']
    order_columns = ['id','nombre','descripcion']
    max_display_length = 100

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.descripcion,
                self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.crear'),
                self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.eliminar')
            ])
        return json_data

    def get_initial_queryset(self):
        return TipoSoporte.objects.exclude(oculto = True)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(nombre__icontains=search) | Q(descripcion__icontains=search)
            qs = qs.filter(q)
        return qs


class ContratosFormadoresView(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cedula
    3.cantidad de contratos
    4.permiso para editar
    """
    model = Formador
    columns = ['id','nombres','cedula']

    order_columns = ['nombres','cedula']
    max_display_length = 100

    def get_initial_queryset(self):
        return Formador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombres + " " + item.apellidos,
                    item.cedula,
                    Contrato.objects.filter(formador = item).count(),
                    self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.editar'),
                ])
        return json_data

class ContratoFormadorView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.fecha creacion
    3.fecha inicio
    4.fecha finalizacion
    5.renuncia
    6.liquidacion
    7.permiso para editar
    """
    model = Contrato
    columns = ['id','nombre','fecha']

    order_columns = ['id','nombre','fecha']
    max_display_length = 100

    def get_initial_queryset(self):
        return Contrato.objects.filter(formador__id = self.kwargs['id_formador'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    item.get_contrato_url(),
                    localtime(item.fecha).strftime('%d de %B del %Y, %X') if item.fecha != None else '',
                    item.fecha_inicio.strftime('%d de %B del %Y') if item.fecha_inicio != None else '',
                    item.fecha_fin.strftime('%d de %B del %Y') if item.fecha_fin != None else '',
                    item.renuncia,
                    item.liquidado,
                    item.get_municipios_string(),
                    item.get_supervisores_string(),
                    self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.editar'),
                ])
        return json_data

class SolicitudSoportesFormadorView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.permiso para editar
    """
    model = SolicitudSoportesFormador
    columns = ['id','nombre']

    order_columns = ['nombre']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_formadores.editar'),
                ])
        return json_data



class ContratosLideresView(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cedula
    3.cantidad de contratos
    4.permiso para editar
    """
    model = Lideres
    columns = ['id','nombres','cedula']

    order_columns = ['nombres','cedula']
    max_display_length = 100

    def get_initial_queryset(self):
        return Lideres.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombres + " " + item.apellidos,
                    item.cedula,
                    ContratoLider.objects.filter(lider = item).count(),
                    self.request.user.has_perm('permisos_sican.rh.rh_contratos_lideres.editar'),
                ])
        return json_data

class ContratoLiderView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.fecha creacion
    3.fecha inicio
    4.fecha finalizacion
    5.renuncia
    6.liquidacion
    7.permiso para editar
    """
    model = ContratoLider
    columns = ['id','nombre','fecha']

    order_columns = ['id','nombre','fecha']
    max_display_length = 100

    def get_initial_queryset(self):
        return ContratoLider.objects.filter(lider__id = self.kwargs['id_lider'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    localtime(item.fecha).strftime('%d de %B del %Y, %X') if item.fecha != None else '',
                    item.fecha_inicio.strftime('%d de %B del %Y') if item.fecha_inicio != None else '',
                    item.fecha_fin.strftime('%d de %B del %Y') if item.fecha_fin != None else '',
                    item.renuncia,
                    item.liquidado,
                    self.request.user.has_perm('permisos_sican.rh.rh_contratos_lideres.editar'),
                ])
        return json_data

class SolicitudSoportesLiderView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.permiso para editar
    """
    model = SolicitudSoportesLider
    columns = ['id','nombre']

    order_columns = ['nombre']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_lideres.editar'),
                ])
        return json_data



class ContratosNegociadoresView(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cedula
    3.cantidad de contratos
    4.permiso para editar
    """
    model = Negociador
    columns = ['id','nombres','cedula']

    order_columns = ['nombres','cedula']
    max_display_length = 100

    def get_initial_queryset(self):
        return Negociador.objects.filter(oculto = False)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombres + " " + item.apellidos,
                    item.cedula,
                    ContratoNegociador.objects.filter(negociador = item).count(),
                    self.request.user.has_perm('permisos_sican.rh.rh_contratos_negociadores.editar'),
                ])
        return json_data

class ContratoNegociadorView(BaseDatatableView):
    """
    0.id
    1.nombres
    2.cedula
    3.cantidad de contratos
    4.permiso para editar
    """
    model = ContratoNegociador
    columns = ['id','nombre','fecha']

    order_columns = ['nombre','fecha']
    max_display_length = 100

    def get_initial_queryset(self):
        return ContratoNegociador.objects.filter(negociador__id = self.kwargs['id_negociador'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    localtime(item.fecha).strftime('%d de %B del %Y, %X'),
                    self.request.user.has_perm('permisos_sican.rh.rh_contratos_negociadores.editar'),
                ])
        return json_data

class SolicitudSoportesNegociadorView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.permiso para editar
    """
    model = SolicitudSoportesNegociador
    columns = ['id','nombre']

    order_columns = ['nombre']
    max_display_length = 100

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombre__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_negociadores.editar'),
                ])
        return json_data


#---------------------------------------------------- CONTRATOS --------------------------------------------------------


class ContratoAdministrativosUserView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.fecha creacion
    3.fecha inicio
    4.fecha finalizacion
    5.renuncia
    6.liquidacion
    7.permiso para editar
    """
    model = ContratoAdministrativo
    columns = ['id','nombre','fecha_inicio','fecha_fin']

    order_columns = ['id','nombre','fecha_inicio','fecha_fin']
    max_display_length = 100

    def get_initial_queryset(self):
        return ContratoAdministrativo.objects.filter(administrativo__usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    localtime(item.fecha).strftime('%d de %B del %Y, %X') if item.fecha != None else '',
                    item.fecha_inicio.strftime('%d de %B del %Y') if item.fecha_inicio != None else '',
                    item.fecha_fin.strftime('%d de %B del %Y') if item.fecha_fin != None else '',
                    item.renuncia,
                    item.liquidado,
                    self.request.user.has_perm('permisos_sican.contratos.contratos_administrativos.editar'),
                ])
        return json_data

class ContratoFormadorUserView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.fecha creacion
    3.fecha inicio
    4.fecha finalizacion
    5.renuncia
    6.liquidacion
    7.permiso para editar
    """
    model = Contrato
    columns = ['id','nombre','fecha_inicio','fecha_fin']

    order_columns = ['id','nombre','fecha_inicio','fecha_fin']
    max_display_length = 100

    def get_initial_queryset(self):
        return Contrato.objects.filter(formador__usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []

        for item in qs:
            json_data.append([
                item.id,
                item.nombre,
                item.get_contrato_url(),
                localtime(item.fecha).strftime('%d de %B del %Y, %X') if item.fecha != None else '',
                item.fecha_inicio.strftime('%d de %B del %Y') if item.fecha_inicio != None else '',
                item.fecha_fin.strftime('%d de %B del %Y') if item.fecha_fin != None else '',
                item.renuncia,
                item.liquidado,
                self.request.user.has_perm('permisos_sican.contratos.contratos_formadores.editar'),
            ])
        return json_data

class ContratoLiderUserView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.fecha creacion
    3.fecha inicio
    4.fecha finalizacion
    5.renuncia
    6.liquidacion
    7.permiso para editar
    """
    model = ContratoLider
    columns = ['id','nombre','fecha_inicio','fecha_fin']

    order_columns = ['id','nombre','fecha_inicio','fecha_fin']
    max_display_length = 100

    def get_initial_queryset(self):
        return ContratoLider.objects.filter(lider__usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    localtime(item.fecha).strftime('%d de %B del %Y, %X') if item.fecha != None else '',
                    item.fecha_inicio.strftime('%d de %B del %Y') if item.fecha_inicio != None else '',
                    item.fecha_fin.strftime('%d de %B del %Y') if item.fecha_fin != None else '',
                    item.renuncia,
                    item.liquidado,
                    self.request.user.has_perm('permisos_sican.contratos.contratos_lideres.editar'),
                ])
        return json_data

class ContratoNegociadorUserView(BaseDatatableView):
    """
    0.id
    1.nombre
    2.fecha creacion
    3.fecha inicio
    4.fecha finalizacion
    5.renuncia
    6.liquidacion
    7.permiso para editar
    """
    model = ContratoNegociador
    columns = ['id','nombre','fecha_inicio','fecha_fin']

    order_columns = ['id','nombre','fecha_inicio','fecha_fin']
    max_display_length = 100

    def get_initial_queryset(self):
        return ContratoNegociador.objects.filter(negociador__usuario = self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            search = unicode(search).capitalize()
            q = Q(nombres__icontains=search)
            qs = qs.filter(q)
        return qs

    def prepare_results(self, qs):
        json_data = []
        stack = []

        for item in qs:

            if item not in stack:
                stack.append(item)

                json_data.append([
                    item.id,
                    item.nombre,
                    localtime(item.fecha).strftime('%d de %B del %Y, %X') if item.fecha != None else '',
                    item.fecha_inicio.strftime('%d de %B del %Y') if item.fecha_inicio != None else '',
                    item.fecha_fin.strftime('%d de %B del %Y') if item.fecha_fin != None else '',
                    item.renuncia,
                    item.liquidado,
                    self.request.user.has_perm('permisos_sican.contratos.contratos_negociadores.editar'),
                ])
        return json_data


#-----------------------------------------------------------------------------------------------------------------------




class BeneficiariosGroupList(BaseDatatableView):
    """
    """
    model = BeneficiarioVigencia
    columns = ['id','cedula','nombres','apellidos','radicado','departamento','municipio']

    order_columns = ['id','cedula','nombres','apellidos','radicado']
    max_display_length = 100


    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(radicado__numero__icontains=search) | Q(apellidos__icontains=search) | \
                Q(nombres__icontains=search) | Q(cedula__icontains=search)
            qs = qs.filter(q)
        return qs

    def get_initial_queryset(self):
        return self.model.objects.filter(grupo__id = self.kwargs['id_grupo'])

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                item.id,
                item.cedula,
                item.nombres,
                item.apellidos,
                item.radicado.numero if item.radicado != None else '',
                item.radicado.municipio.departamento.nombre if item.radicado != None else '',
                item.radicado.municipio.nombre if item.radicado != None else '',
                item.correo,
                item.telefono_fijo,
                item.telefono_celular,
                item.area,
                item.grado,
                item.genero,
                item.estado,
                self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.editar'),
                self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.ocultar'),
            ])
        return json_data