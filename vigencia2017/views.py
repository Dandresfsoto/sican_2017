#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from vigencia2017.models import DaneSEDE, TipoContrato, ValorEntregableVigencia2017, CargaMatriz
from vigencia2017.forms import DaneSEDEForm, GruposForm, TipoContratoForm, ValorEntregableVigencia2017Form, CargaMatrizForm
from formadores.models import Contrato, Grupos
from productos.models import Entregable
from productos.models import Diplomado
from vigencia2017.tasks import carga_masiva_matrices
from vigencia2017.models import Grupos as GruposVigencia2017
from vigencia2017.models import Beneficiario as BeneficiarioVigencia2017
from vigencia2017.forms import BeneficiarioVigencia2017Form, NewBeneficiarioVigencia2017Form, SubsanacionEvidenciaForm
from vigencia2017.models import Evidencia as EvidenciaVigencia2017
from vigencia2017.forms import EvidenciaVigencia2017Form, GruposVigencia2017ConectividadForm, MasivoVigencia2017Form
from vigencia2017.models import Evidencia, Red
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from vigencia2017.models import Pago as PagoVigencia2017
import shutil
from vigencia2017.models import CargaMasiva2017
from django.core.files.uploadedfile import SimpleUploadedFile
from zipfile import ZipFile
from vigencia2017.forms import RedForm
from region.models import Region
from django.shortcuts import HttpResponseRedirect
from vigencia2017.tasks import build_red
from vigencia2017.models import Corte as CorteVigencia2017
from vigencia2017.forms import CorteVigencia2017Form
from django.db.models import Sum
import locale
from informes.functions import construir_reporte
import datetime
import pytz
from django.core.files import File
from vigencia2017.tasks import set_pago
import json
from django.shortcuts import render_to_response
from django.template import RequestContext

from vigencia2017.tasks import carga_masiva_evidencia
from vigencia2017.tasks import retroalimentacion_red
from vigencia2017.forms import RedRetroalimentacionForm
import os
from vigencia2017.models import Subsanacion, Rechazo

# Create your views here.
class ListadoCodigosDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/dane/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_dane.informes')
        return super(ListadoCodigosDaneView, self).get_context_data(**kwargs)


class NuevoCodigoDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = DaneSEDE
    form_class = DaneSEDEForm
    success_url = '../'
    template_name = 'vigencia2017/dane/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.crear"


class UpdateCodigoDaneView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = DaneSEDE
    form_class = DaneSEDEForm
    success_url = '../../'
    template_name = 'vigencia2017/dane/editar.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_dane.editar"


    def get_context_data(self, **kwargs):
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        return super(UpdateCodigoDaneView, self).get_context_data(**kwargs)









class ListadoGruposFormacionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.informes')
        return super(ListadoGruposFormacionView, self).get_context_data(**kwargs)




class ListadoGruposFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_formador.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.informes')
        kwargs['id_contrato'] = self.kwargs['pk']
        return super(ListadoGruposFormadorView, self).get_context_data(**kwargs)


class NuevoGrupoFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = Grupos
    form_class = GruposForm
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.crear"


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Contrato.objects.get(id = self.kwargs['pk']).formador.get_full_name()
        return super(NuevoGrupoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk']}










class ListadoValorContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/valor_contratos/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear')
        return super(ListadoValorContratosView, self).get_context_data(**kwargs)



class NuevoValorContratoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = TipoContrato
    form_class = TipoContratoForm
    success_url = '../'
    template_name = 'vigencia2017/valor_contratos/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear"



class ValorProductosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         FormView):

    form_class = ValorEntregableVigencia2017Form
    success_url = '../../../'
    template_name = 'vigencia2017/valor_contratos/valor_diplomado.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_valor_contratos.crear"

    def get_context_data(self, **kwargs):
        kwargs['contrato'] = TipoContrato.objects.get(id = self.kwargs['id_contrato']).nombre
        kwargs['diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        return super(ValorProductosView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['id_contrato'],'id_diplomado':self.kwargs['id_diplomado']}

    def form_valid(self, form):

        entregables = Entregable.objects.filter(sesion__nivel__diplomado__id=self.kwargs['id_diplomado']).order_by('numero')
        tipo_contrato = TipoContrato.objects.get(id = self.kwargs['id_contrato'])

        for entregable in entregables:
            valor, created = ValorEntregableVigencia2017.objects.get_or_create(entregable = entregable,tipo_contrato = tipo_contrato)
            valor.valor = form.cleaned_data[str(entregable.id)]
            valor.save()

        return super(ValorProductosView, self).form_valid(form)



class ListadoCargaMatrizView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/cargar_matriz/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.crear')
        return super(ListadoCargaMatrizView, self).get_context_data(**kwargs)




class NuevaCargaMatrizView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = CargaMatriz
    form_class = CargaMatrizForm
    success_url = '../'
    template_name = 'vigencia2017/cargar_matriz/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.crear"

    def get_initial(self):
        return {'id_usuario':self.request.user.id}

    def form_valid(self, form):
        self.object = form.save()
        carga_masiva_matrices.delay(self.object.id,self.request.user.email)
        return super(NuevaCargaMatrizView, self).form_valid(form)



class ListadoInscritosGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_inscritos.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        return super(ListadoInscritosGrupoView, self).get_context_data(**kwargs)



class EditarBeneficiarioGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = BeneficiarioVigencia2017
    form_class = BeneficiarioVigencia2017Form
    pk_url_kwarg = 'id_beneficiario'
    success_url = '../../'
    template_name = 'vigencia2017/grupos_formacion/editar_beneficiario.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.editar"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['cedula'] = BeneficiarioVigencia2017.objects.get(id=self.kwargs['id_beneficiario']).cedula
        return super(EditarBeneficiarioGrupoView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo']}


class NuevoBeneficiarioGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = BeneficiarioVigencia2017
    form_class = NewBeneficiarioVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nuevo_beneficiario.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.editar"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        return super(NuevoBeneficiarioGrupoView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo']}





class ListadoCambioMatrizView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/cargar_matriz/lista_cambios.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cargar_matriz.ver"


    def get_context_data(self, **kwargs):
        kwargs['id_matriz'] = self.kwargs['pk']
        return super(ListadoCambioMatrizView, self).get_context_data(**kwargs)




class ArbolDiplomadoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/arbol.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['diplomado'] = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo']).diplomado.nombre
        return super(ArbolDiplomadoView, self).get_context_data(**kwargs)





class ListaEvidenciasEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/grupos_formacion/lista_evidencias.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['diplomado'] = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo']).diplomado.nombre
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear')
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(ListaEvidenciasEntregableView, self).get_context_data(**kwargs)






class NuevaEvidenciasEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         CreateView):
    model = EvidenciaVigencia2017
    form_class = EvidenciaVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/nueva_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(NuevaEvidenciasEntregableView, self).get_context_data(**kwargs)

    def form_valid(self, form):


        if 'archivo' in form.cleaned_data.keys():

            self.object = form.save()


        else:
            output = StringIO.StringIO()
            output.write(form.cleaned_data['link'])

            output.seek(0,2)
            file_data = InMemoryUploadedFile(output, 'file', 'link.txt', None, output.tell(), None)

            self.object = form.save(commit=False)
            self.object.archivo = file_data
            self.object.save()


        cargados = self.object.beneficiarios_cargados.all()
        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(contrato=contrato, entregable=entregable).filter(
                beneficiarios_cargados__id__in=cargados.values_list('id', flat=True)).distinct()

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)
                cargado.delete_pago_entregable(id_entregable=evidencia.entregable.id)


        for cargado in form.cleaned_data['beneficiarios_cargados']:
            self.object.beneficiarios_cargados.add(cargado)
            cargado.set_pago_entregable(id_entregable=self.object.entregable.id,evidencia_id=self.object.id)


        return super(NuevaEvidenciasEntregableView,self).form_valid(form)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo'],
                'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}







class MasivoEvidenciasEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         FormView):
    form_class = MasivoVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/masivo_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(MasivoEvidenciasEntregableView, self).get_context_data(**kwargs)


    def form_valid(self, form):

        context = self.get_context_data()


        carga = CargaMasiva2017.objects.create(archivo=form.cleaned_data['archivo'])

        #carga_masiva_evidencia.delay(carga.id,self.kwargs['pk'],self.kwargs['id_entregable'],self.request.user.id)


        user = self.request.user
        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])

        soportes = ZipFile(carga.archivo, 'r')

        resultados = []

        cantidad_cargados = 0
        cantidad_rechazados = 0

        for soporte_info in soportes.infolist():
            soporte = soporte_info.filename
            archivo = SimpleUploadedFile(name=soporte, content=soportes.read(soporte_info))
            resultado = ""

            try:
                cedula = soporte.split('/')[-1].split('.')[-2]
            except:
                pass
            else:
                try:
                    beneficiario = BeneficiarioVigencia2017.objects.get(cedula=cedula)
                except:
                    resultado = "La cedula no esta registrada en el sistema"
                    cantidad_rechazados += 1
                else:
                    if beneficiario.grupo.contrato == contrato:
                        evidencias = EvidenciaVigencia2017.objects.filter(entregable=entregable, contrato=beneficiario.grupo.contrato)

                        if evidencias.filter(beneficiarios_validados=beneficiario).count() == 0:
                            #si la evidencia no esta validada
                            cuenta_reportadas = 0
                            if evidencias.filter(beneficiarios_cargados=beneficiario).count() > 0:
                                #si la evidencia esta cargada
                                evidencias_cargadas = evidencias.filter(beneficiarios_cargados=beneficiario)
                                for evidencia_cargada in evidencias_cargadas:
                                    if evidencia_cargada.red_id == None:
                                        #si la evidencia no esta reportada
                                        evidencia_cargada.beneficiarios_cargados.remove(beneficiario)
                                        beneficiario.delete_pago_entregable(id_entregable=entregable.id)
                                    else:
                                        #si la evidencia esta reportada
                                        resultado = "La evidencia fue reportada en el RED-VIG2017-" + str(evidencia_cargada.red_id)
                                        cuenta_reportadas += 1
                            if cuenta_reportadas == 0:
                                evidencia = self.create_evidencia(archivo, user, entregable, beneficiario)
                                resultado = "La evidencia se cargo exitosamente con el codigo SIC-" + str(evidencia.id)
                                cantidad_cargados += 1
                            else:
                                cantidad_rechazados += 1

                        else:
                            # si la evidencia esta validada
                            resultado = "La evidencia ya fue aprobada y no es necesario cargarla nuevamente"
                            cantidad_rechazados += 1
                    else:
                        resultado = "La cedula no corresponde a un beneficiario del contrato"
                        cantidad_rechazados += 1

            resultados.append({'cedula': cedula, 'resultado': resultado})

        context['resultados'] = resultados
        context['cantidad_cargados'] = cantidad_cargados
        context['cantidad_rechazados'] = cantidad_rechazados

        return render_to_response('vigencia2017/grupos_formacion/resultado_masivo.html',context,context_instance=RequestContext(self.request))


    def create_evidencia(self,archivo,user,entregable,beneficiario):
        evidencia = EvidenciaVigencia2017.objects.create(usuario=user,
                                                         archivo=archivo,
                                                         entregable=entregable,
                                                         contrato=beneficiario.grupo.contrato)
        evidencia.beneficiarios_cargados.add(beneficiario)
        beneficiario.set_pago_entregable(id_entregable=entregable.id, evidencia_id=evidencia.id)
        return evidencia



class MasivoEvidenciasEntregableNoPagoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         FormView):
    form_class = MasivoVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/grupos_formacion/masivo_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.crear"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(MasivoEvidenciasEntregableNoPagoView, self).get_context_data(**kwargs)


    def form_valid(self, form):

        context = self.get_context_data()


        carga = CargaMasiva2017.objects.create(archivo=form.cleaned_data['archivo'])

        #carga_masiva_evidencia.delay(carga.id,self.kwargs['pk'],self.kwargs['id_entregable'],self.request.user.id)


        user = self.request.user
        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])

        soportes = ZipFile(carga.archivo, 'r')

        resultados = []

        cantidad_cargados = 0
        cantidad_rechazados = 0

        for soporte_info in soportes.infolist():
            soporte = soporte_info.filename
            archivo = SimpleUploadedFile(name=soporte, content=soportes.read(soporte_info))
            resultado = ""

            try:
                cedula = soporte.split('/')[-1].split('.')[-2]
            except:
                pass
            else:
                try:
                    beneficiario = BeneficiarioVigencia2017.objects.get(cedula=cedula)
                except:
                    resultado = "La cedula no esta registrada en el sistema"
                    cantidad_rechazados += 1
                else:
                    if beneficiario.grupo.contrato == contrato:
                        evidencias = EvidenciaVigencia2017.objects.filter(entregable=entregable, contrato=beneficiario.grupo.contrato)

                        if evidencias.filter(beneficiarios_validados=beneficiario).count() == 0:
                            #si la evidencia no esta validada
                            cuenta_reportadas = 0
                            if evidencias.filter(beneficiarios_cargados=beneficiario).count() > 0:
                                #si la evidencia esta cargada
                                evidencias_cargadas = evidencias.filter(beneficiarios_cargados=beneficiario)
                                for evidencia_cargada in evidencias_cargadas:
                                    if evidencia_cargada.red_id == None:
                                        #si la evidencia no esta reportada
                                        evidencia_cargada.beneficiarios_cargados.remove(beneficiario)
                                    else:
                                        #si la evidencia esta reportada
                                        resultado = "La evidencia fue reportada en el RED-VIG2017-" + str(evidencia_cargada.red_id)
                                        cuenta_reportadas += 1
                            if cuenta_reportadas == 0:
                                evidencia = self.create_evidencia(archivo, user, entregable, beneficiario)
                                resultado = "La evidencia se cargo exitosamente con el codigo SIC-" + str(evidencia.id)
                                cantidad_cargados += 1
                            else:
                                cantidad_rechazados += 1

                        else:
                            # si la evidencia esta validada
                            resultado = "La evidencia ya fue aprobada y no es necesario cargarla nuevamente"
                            cantidad_rechazados += 1
                    else:
                        resultado = "La cedula no corresponde a un beneficiario del contrato"
                        cantidad_rechazados += 1

            resultados.append({'cedula': cedula, 'resultado': resultado})

        context['resultados'] = resultados
        context['cantidad_cargados'] = cantidad_cargados
        context['cantidad_rechazados'] = cantidad_rechazados

        return render_to_response('vigencia2017/grupos_formacion/resultado_masivo.html',context,context_instance=RequestContext(self.request))


    def create_evidencia(self,archivo,user,entregable,beneficiario):
        evidencia = EvidenciaVigencia2017.objects.create(usuario=user,
                                                         archivo=archivo,
                                                         entregable=entregable,
                                                         contrato=beneficiario.grupo.contrato)
        evidencia.beneficiarios_cargados.add(beneficiario)
        return evidencia



class EditarEvidenciaEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = EvidenciaVigencia2017
    form_class = EvidenciaVigencia2017Form
    success_url = '../../'
    pk_url_kwarg = 'id_evidencia'
    template_name = 'vigencia2017/grupos_formacion/editar_evidencia.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.editar"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['codigo_dane'] = DaneSEDE.objects.get(id=self.kwargs['pk']).dane_sede
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['id_evidencia'] = self.kwargs['id_evidencia']
        kwargs['nombre_entregable'] = Entregable.objects.get(id=self.kwargs['id_entregable']).nombre
        return super(EditarEvidenciaEntregableView, self).get_context_data(**kwargs)

    def form_valid(self, form):

        for cargado in self.object.beneficiarios_cargados.all():
            cargado.delete_pago_entregable(id_entregable = self.object.entregable.id)


        if 'archivo' in form.cleaned_data.keys():

            self.object = form.save()


        else:
            output = StringIO.StringIO()
            output.write(form.cleaned_data['link'])

            output.seek(0,2)
            file_data = InMemoryUploadedFile(output, 'file', 'link.txt', None, output.tell(), None)

            self.object = form.save(commit=False)
            self.object.archivo = file_data
            self.object.save()



        cargados = self.object.beneficiarios_cargados.all()

        for cargado in cargados:
            cargado.delete_pago_entregable(id_entregable = self.object.entregable.id)


        contrato = Contrato.objects.get(id=self.kwargs['pk'])
        entregable = Entregable.objects.get(id=self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(contrato=contrato, entregable=entregable).filter(
                beneficiarios_cargados__id__in=cargados.values_list('id', flat=True)).distinct()

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)
                cargado.delete_pago_entregable(id_entregable=evidencia.entregable.id)


        for cargado in form.cleaned_data['beneficiarios_cargados']:
            self.object.beneficiarios_cargados.add(cargado)
            cargado.set_pago_entregable(id_entregable=self.object.entregable.id, evidencia_id=self.object.id)

        return super(EditarEvidenciaEntregableView,self).form_valid(form)

    def get_initial(self):
        return {'id_contrato':self.kwargs['pk'],'id_grupo':self.kwargs['id_grupo'],
                'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}









class DeleteEvidenciaEntregableView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         DeleteView):
    model = EvidenciaVigencia2017
    success_url = '../../'
    pk_url_kwarg = 'id_evidencia'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_evidencias.eliminar"

    def get(self, request, *args, **kwargs):

        evidencia = Evidencia.objects.get(id = kwargs['id_evidencia'])

        for cargado in evidencia.beneficiarios_cargados.all():
            cargado.delete_pago_entregable(id_entregable = evidencia.entregable.id)
        return self.post(request, *args, **kwargs)




class ConectividadGrupoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         UpdateView):
    model = GruposVigencia2017
    form_class = GruposVigencia2017ConectividadForm
    pk_url_kwarg = 'id_grupo'
    success_url = '../../'
    template_name = 'vigencia2017/grupos_formacion/no_conectividad.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"


    def get_context_data(self, **kwargs):
        grupo = GruposVigencia2017.objects.get(id=self.kwargs['id_grupo'])
        kwargs['formador'] = Contrato.objects.get(id=self.kwargs['pk']).formador.get_full_name()
        kwargs['codigo_grupo'] = grupo.diplomado.nombre + ": " + grupo.get_nombre_grupo()
        kwargs['id_contrato'] = self.kwargs['pk']
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_grupos.crear')
        return super(ConectividadGrupoView, self).get_context_data(**kwargs)


    def form_valid(self, form):
        self.object = form.save()

        archivo = form.cleaned_data['archivo']

        if archivo == None or archivo == False:
            self.object.no_conectividad = False
        else:
            self.object.no_conectividad = True

        self.object.save()

        return super(ConectividadGrupoView , self).form_valid(form)





class EvidenciasListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/evidencias/codigos/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_codigos.ver"

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_codigos.informes')
        return super(EvidenciasListView,self).get_context_data(**kwargs)



class BeneficiarioEvidenciaCedulaList(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/evidencias/cedula/lista_beneficiarios.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cedula_beneficiario.ver"



class BeneficiarioEvidenciaCedulaProductoList(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/evidencias/cedula/lista_productos.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cedula_beneficiario.ver"


    def get_context_data(self, **kwargs):
        kwargs['id_beneficiario'] = self.kwargs['id_beneficiario']
        kwargs['nombre_beneficiario'] = BeneficiarioVigencia2017.objects.get(id = self.kwargs['id_beneficiario']).get_full_name()
        return super(BeneficiarioEvidenciaCedulaProductoList,self).get_context_data(**kwargs)





class RedsListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/red/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_reds.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_reds.crear')
        return super(RedsListView,self).get_context_data(**kwargs)





class NuevoRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Red
    form_class = RedForm
    success_url = '../'
    template_name = 'vigencia2017/red/nuevo.html'
    permission_required = "permisos_sican.evidencias.red.crear"

    def get_context_data(self, **kwargs):

        evidencias = Evidencia.objects.filter(red_id = None,entregable__escencial = "Si")

        region_1 = Region.objects.get(numero = 1)
        region_2 = Region.objects.get(numero = 2)

        evidencias_r1 = evidencias.filter(contrato__region = region_1)
        evidencias_r2 = evidencias.filter(contrato__region = region_2)

        evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')
        evidencias_r1_escuelatic_innovadores = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='ESCUELATIC DOCENTES INNOVADORES')
        evidencias_r1_docentic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='DOCENTIC')
        evidencias_r1_san_andres = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='SAN ANDRES')


        evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')
        evidencias_r2_escuelatic_innovadores = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='ESCUELATIC DOCENTES INNOVADORES')
        evidencias_r2_docentic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='DOCENTIC')

        kwargs['formadores_innovatic_r1'] = evidencias_r1_innovatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r1'] = evidencias_r1_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r1'] = evidencias_r1_innovatic.count()

        kwargs['formadores_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r1'] = evidencias_r1_tecnotic.count()

        kwargs['formadores_directic_r1'] = evidencias_r1_directic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r1'] = evidencias_r1_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r1'] = evidencias_r1_directic.count()

        kwargs['formadores_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r1'] = evidencias_r1_escuelatic.count()

        kwargs['formadores_docentes_innovadores_r1'] = evidencias_r1_escuelatic_innovadores.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_docentes_innovadores_r1'] = evidencias_r1_escuelatic_innovadores.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_docentes_innovadores_r1'] = evidencias_r1_escuelatic_innovadores.count()

        kwargs['formadores_docentic_r1'] = evidencias_r1_docentic.values_list('contrato__formador', flat=True).distinct().count()
        kwargs['beneficiarios_docentic_r1'] = evidencias_r1_docentic.values_list('beneficiarios_cargados', flat=True).distinct().count()
        kwargs['evidencias_docentic_r1'] = evidencias_r1_docentic.count()

        kwargs['formadores_san_andres_r1'] = evidencias_r1_san_andres.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_san_andres_r1'] = evidencias_r1_san_andres.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_san_andres_r1'] = evidencias_r1_san_andres.count()



        kwargs['formadores_innovatic_r2'] = evidencias_r2_innovatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r2'] = evidencias_r2_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r2'] = evidencias_r2_innovatic.count()

        kwargs['formadores_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r2'] = evidencias_r2_tecnotic.count()

        kwargs['formadores_directic_r2'] = evidencias_r2_directic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r2'] = evidencias_r2_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r2'] = evidencias_r2_directic.count()

        kwargs['formadores_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r2'] = evidencias_r2_escuelatic.count()

        kwargs['formadores_docentes_innovadores_r2'] = evidencias_r2_escuelatic_innovadores.values_list('contrato__formador', flat=True).distinct().count()
        kwargs['beneficiarios_docentes_innovadores_r2'] = evidencias_r2_escuelatic_innovadores.values_list('beneficiarios_cargados', flat=True).distinct().count()
        kwargs['evidencias_docentes_innovadores_r2'] = evidencias_r2_escuelatic_innovadores.count()

        kwargs['formadores_docentic_r2'] = evidencias_r2_docentic.values_list('contrato__formador',flat=True).distinct().count()
        kwargs['beneficiarios_docentic_r2'] = evidencias_r2_docentic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_docentic_r2'] = evidencias_r2_docentic.count()

        return super(NuevoRedView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        red = Red.objects.get(id = self.object.id)

        if not red.producto_final:
            evidencias = Evidencia.objects.filter(red_id=None, entregable__escencial="Si")

            region_1 = Region.objects.get(numero = 1)
            region_2 = Region.objects.get(numero = 2)

            evidencias_r1 = evidencias.filter(contrato__region = region_1)
            evidencias_r2 = evidencias.filter(contrato__region = region_2)

            evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='INNOVATIC')
            evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='TECNOTIC')
            evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='DIRECTIC')
            evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='ESCUELA TIC FAMILIA')
            evidencias_r1_escuelatic_innovadores = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='ESCUELATIC DOCENTES INNOVADORES')
            evidencias_r1_docentic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='DOCENTIC')
            evidencias_r1_san_andres = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre='SAN ANDRES')

            evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='INNOVATIC')
            evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='TECNOTIC')
            evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='DIRECTIC')
            evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='ESCUELA TIC FAMILIA')
            evidencias_r2_escuelatic_innovadores = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='ESCUELATIC DOCENTES INNOVADORES')
            evidencias_r2_docentic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre='DOCENTIC')



            if self.object.region.numero == 1:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    evidencias_r1_innovatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'TECNOTIC':
                    evidencias_r1_tecnotic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DIRECTIC':
                    evidencias_r1_directic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                    evidencias_r1_escuelatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELATIC DOCENTES INNOVADORES':
                    evidencias_r1_escuelatic_innovadores.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DOCENTIC':
                    evidencias_r1_docentic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'SAN ANDRES':
                    evidencias_r1_san_andres.update(red_id = red.id)
                else:
                    pass

            elif self.object.region.numero == 2:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    evidencias_r2_innovatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'TECNOTIC':
                    evidencias_r2_tecnotic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DIRECTIC':
                    evidencias_r2_directic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                    evidencias_r2_escuelatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELATIC DOCENTES INNOVADORES':
                    evidencias_r2_escuelatic_innovadores.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DOCENTIC':
                    evidencias_r2_docentic.update(red_id = red.id)
                else:
                    pass


            else:
                pass
            red.save()
            build_red.delay(red.id)
        else:

            pass
        return HttpResponseRedirect(self.get_success_url())




class ListadoCortesPago(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/cortes_pago/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cortes_pago.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.vigencia_2017.vigencia_2017_cortes_pago.crear')
        return super(ListadoCortesPago,self).get_context_data(**kwargs)




class NuevoCortePago(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):
    form_class = CorteVigencia2017Form
    success_url = '../'
    template_name = 'vigencia2017/cortes_pago/nuevo.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_cortes_pago.crear"

    def form_valid(self, form):

        corte = CorteVigencia2017.objects.create()
        titulos = ['Región','Formador','Contrato','Cedula','Valor']
        formatos = ['General', 'General', 'General', '0', '$ #,##0.00']
        ancho_columnas = [30, 50, 50, 20, 60]
        contenidos = []

        contratos = Contrato.objects.filter(vigencia="vigencia2017").exclude(tipo_contrato_id=None)

        ids = []
        for diplomado in Diplomado.objects.all():
            ids += form.cleaned_data['diplomado_' + str(diplomado.id)]

        for contrato in contratos:
            pagos = PagoVigencia2017.objects.filter(corte_id = None,beneficiario__grupo__contrato = contrato,entregable__id__in = ids)
            valor = pagos.aggregate(Sum('valor')).get('valor__sum','0.0')

            if valor == None:
                valor = 0.0


            if form.cleaned_data[str(contrato.id)] == True:
                id_pagos = json.dumps(list(pagos.values_list('id',flat=True)))
                set_pago.delay(id_pagos,corte.id)


                contenidos.append([contrato.get_region().nombre,contrato.formador.get_full_name(),contrato.nombre,contrato.formador.cedula,valor])

        fecha = pytz.utc.localize(datetime.datetime.now())
        output = construir_reporte(titulos, contenidos, formatos, ancho_columnas, 'CORTE DE PAGO', fecha, self.request.user, 'FIN-01')




        filename = 'CORTE-' + unicode(corte.id) + '.xlsx'

        corte.archivo.save(filename, File(output))

        return super(NuevoCortePago, self).form_valid(form)





class RendimientoCargaEvidencias(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/rendimiento_evidencias/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_rendimiento.ver"



class ResumenEvidencias(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/resumen_evidencias/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_resumen_evidencias.ver"



class InformacionContrato(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/informacion_contrato/contrato.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_grupos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = Contrato.objects.get(id=self.kwargs['id_contrato']).nombre
        kwargs['id_contrato'] = self.kwargs['id_contrato']
        kwargs['nombre_formador'] = Contrato.objects.get(id=self.kwargs['id_contrato']).formador.get_full_name()
        return super(InformacionContrato,self).get_context_data(**kwargs)


class UpdateRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Red
    form_class = RedRetroalimentacionForm
    success_url = '../../'
    template_name = 'vigencia2017/red/editar.html'
    permission_required = "permisos_sican.evidencias.red.editar"


    def form_valid(self, form):
        self.object = form.save()
        retroalimentacion_red.delay(self.object.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        kwargs['id_red'] = self.kwargs['pk']
        return super(UpdateRedView, self).get_context_data(**kwargs)


class TableroControl(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/tablero_control/tablero.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_resumen_evidencias.ver"



class SubsanacionEvidencias(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/subsanacion_evidencias/lista.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_subsanacion_evidencias.ver"




class ListaSubsanacionEvidencias(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'vigencia2017/subsanacion_evidencias/lista_evidencias.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_subsanacion_evidencias.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_evidencia'] = self.kwargs['pk']
        return super(ListaSubsanacionEvidencias, self).get_context_data(**kwargs)



class SubsanacionEvidenciasFormView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):

    form_class = SubsanacionEvidenciaForm
    success_url = '../'
    template_name = 'vigencia2017/subsanacion_evidencias/subsanacion.html'
    permission_required = "permisos_sican.vigencia_2017.vigencia_2017_subsanacion_evidencias.ver"

    def get_context_data(self, **kwargs):

        evidencia = Evidencia.objects.get(id = self.kwargs['pk'])

        kwargs['id_evidencia'] = self.kwargs['pk']
        kwargs['link_soporte'] = evidencia.get_archivo_url()
        kwargs['nombre_soporte'] = os.path.basename(evidencia.archivo.name)

        return super(SubsanacionEvidenciasFormView,self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_evidencia':self.kwargs['pk']}

    def form_valid(self, form):
        keys = list(form.cleaned_data.keys())
        keys.remove('archivo')
        keys.remove('observacion')

        evidencia = Evidencia.objects.get(id = self.kwargs['pk'])


        if form.cleaned_data['archivo'] != None:
            archivo = form.cleaned_data['archivo']
        else:
            archivo = evidencia.archivo

        nueva_evidencia = Evidencia.objects.create(usuario = self.request.user,archivo = archivo,entregable=evidencia.entregable,
                                                   contrato=evidencia.contrato,subsanacion=True)

        cantidad = 0

        for key in keys:
            if form.cleaned_data[key]:
                cantidad += 1
                beneficiario = BeneficiarioVigencia2017.objects.get(id = key.split('_')[1])
                nueva_evidencia.beneficiarios_cargados.add(beneficiario)
                rechazo = Rechazo.objects.filter(evidencia_id__exact = self.kwargs['pk'],beneficiario_rechazo = beneficiario)

                try:
                    evidencia.beneficiarios_cargados.remove(beneficiario)
                except:
                    pass
                try:
                    evidencia.beneficiarios_rechazados.remove(rechazo[0])
                except:
                    pass

        nueva_evidencia.cantidad_cargados = cantidad
        nueva_evidencia.save()

        Subsanacion.objects.create(evidencia_origen = evidencia,evidencia_subsanada=nueva_evidencia,usuario=self.request.user,
                                   observacion = form.cleaned_data['observacion'])

        if evidencia.beneficiarios_rechazados.all().count() == 0:
            evidencia.subsanacion = True
            evidencia.save()

        return super(SubsanacionEvidenciasFormView,self).form_valid(form)
