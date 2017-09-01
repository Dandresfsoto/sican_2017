#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import Diplomado, Nivel, Sesion
from formadores.models import Formador
from evidencias.models import Evidencia
from evidencias.forms import EvidenciaForm
from productos.models import Entregable
from evidencias.models import Red, Subsanacion
from evidencias.forms import RedForm, RedRetroalimentacionForm
from region.models import Region
from django.shortcuts import HttpResponseRedirect
from evidencias.tasks import build_red, carga_masiva_evidencias, retroalimentacion_red, build_red_producto_final
from evidencias.models import CargaMasiva
from evidencias.forms import CargaMasivaForm
from matrices.models import Beneficiario
from django.views.generic import FormView
from evidencias.forms import SubsanacionEvidenciaForm
from matrices.forms import BeneficiarioUpdateForm
import os
from radicados.models import Radicado
from evidencias.models import Rechazo
from matrices.forms import PleBeneficiarioForm
import codecs
from sican.settings import base as settings
from django.core.files import File
import random

# Create your views here.

class DiplomadosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_diplomados.html'
    permission_required = "permisos_sican.evidencias.general.ver"


class DiplomadosActividadesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/actividades/lista_diplomados.html'
    permission_required = "permisos_sican.evidencias.codigos_evidencia.ver"


class FormadoresListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_formadores.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.general.informes')
        return super(FormadoresListView,self).get_context_data(**kwargs)



class ActividadesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/actividades/lista_actividades.html'
    permission_required = "permisos_sican.evidencias.codigos_evidencia.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.general.informes')
        return super(ActividadesListView,self).get_context_data(**kwargs)



class BeneficiariosEvidenciaListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/actividades/lista_beneficiarios.html'
    permission_required = "permisos_sican.evidencias.codigos_evidencia.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_actividad'] = self.kwargs['id_evidencia']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_actividad'] = Entregable.objects.get(id = self.kwargs['id_evidencia']).nombre
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.codigos_evidencia.informes')
        return super(BeneficiariosEvidenciaListView,self).get_context_data(**kwargs)



class NivelesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_niveles.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.general.informes')
        return super(NivelesListView,self).get_context_data(**kwargs)



class SesionesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_sesiones.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        return super(SesionesListView,self).get_context_data(**kwargs)


class EntregablesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_entregables.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        return super(EntregablesListView,self).get_context_data(**kwargs)



class SoportesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/general/lista_soportes.html'
    permission_required = "permisos_sican.evidencias.general.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(SoportesListView,self).get_context_data(**kwargs)


class NuevoSoporteView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Evidencia
    form_class = EvidenciaForm
    success_url = '../'
    template_name = 'evidencias/general/nuevo.html'
    permission_required = "permisos_sican.evidencias.general.crear"

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador'],'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(NuevoSoporteView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        cargados = self.object.beneficiarios_cargados.all()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])
        entregable = Entregable.objects.get(id = self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable).filter(beneficiarios_cargados__id__in = cargados.values_list('id',flat=True))

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)

        return super(NuevoSoporteView,self).form_valid(form)


class UpdateSoporteView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Evidencia
    form_class = EvidenciaForm
    success_url = '../../'
    pk_url_kwarg = 'id_soporte'
    template_name = 'evidencias/general/nuevo.html'
    permission_required = "permisos_sican.evidencias.general.editar"

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador'],'id_entregable':self.kwargs['id_entregable'],'id_usuario':self.request.user.id}

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(UpdateSoporteView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        cargados = self.object.beneficiarios_cargados.all()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])
        entregable = Entregable.objects.get(id = self.kwargs['id_entregable'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable).filter(beneficiarios_cargados__id__in = cargados.values_list('id',flat=True))

        for evidencia in evidencias:
            for cargado in cargados:
                evidencia.beneficiarios_cargados.remove(cargado)

        return super(UpdateSoporteView,self).form_valid(form)


class DeleteSoporteView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Evidencia
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'evidencias/general/eliminar.html'
    permission_required = "permisos_sican.evidencias.general.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['id_diplomado'] = self.kwargs['id_diplomado']
        kwargs['id_nivel'] = self.kwargs['id_nivel']
        kwargs['id_sesion'] = self.kwargs['id_sesion']
        kwargs['nombre_diplomado'] = Diplomado.objects.get(id = self.kwargs['id_diplomado']).nombre
        kwargs['nombre_nivel'] = Nivel.objects.get(id = self.kwargs['id_nivel']).nombre
        kwargs['nombre_sesion'] = Sesion.objects.get(id = self.kwargs['id_sesion']).nombre
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_entregable'] = self.kwargs['id_entregable']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.general.crear')
        return super(DeleteSoporteView,self).get_context_data(**kwargs)



class EvidenciasListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/codigos/lista.html'
    permission_required = "permisos_sican.evidencias.codigos.ver"

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.evidencias.codigos.informes')
        return super(EvidenciasListView,self).get_context_data(**kwargs)


class RedsListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/red/lista.html'
    permission_required = "permisos_sican.evidencias.red.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.red.crear')
        return super(RedsListView,self).get_context_data(**kwargs)


class NuevoRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Red
    form_class = RedForm
    success_url = '../'
    template_name = 'evidencias/red/nuevo.html'
    permission_required = "permisos_sican.evidencias.red.crear"

    def get_context_data(self, **kwargs):

        evidencias = Evidencia.objects.filter(red_id = None)

        region_1 = Region.objects.get(numero = 1)
        region_2 = Region.objects.get(numero = 2)

        evidencias_r1 = evidencias.filter(formador__region = region_1)
        evidencias_r2 = evidencias.filter(formador__region = region_2)

        evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')

        evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
        evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
        evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
        evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')

        ple_r1 = Beneficiario.objects.filter(region__id=1,estado_producto_final='cargado')
        ple_r2 = Beneficiario.objects.filter(region__id=2, estado_producto_final='cargado')


        kwargs['formadores_innovatic_r1'] = evidencias_r1_innovatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r1'] = evidencias_r1_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r1'] = evidencias_r1_innovatic.count()

        kwargs['formadores_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r1'] = evidencias_r1_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r1'] = evidencias_r1_tecnotic.count()

        kwargs['formadores_directic_r1'] = evidencias_r1_directic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r1'] = evidencias_r1_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r1'] = evidencias_r1_directic.count()

        kwargs['formadores_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r1'] = evidencias_r1_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r1'] = evidencias_r1_escuelatic.count()

        kwargs['formadores_innovatic_r2'] = evidencias_r2_innovatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_innovatic_r2'] = evidencias_r2_innovatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_innovatic_r2'] = evidencias_r2_innovatic.count()

        kwargs['formadores_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_tecnotic_r2'] = evidencias_r2_tecnotic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_tecnotic_r2'] = evidencias_r2_tecnotic.count()

        kwargs['formadores_directic_r2'] = evidencias_r2_directic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_directic_r2'] = evidencias_r2_directic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_directic_r2'] = evidencias_r2_directic.count()

        kwargs['formadores_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('formador',flat=True).distinct().count()
        kwargs['beneficiarios_escuelatic_r2'] = evidencias_r2_escuelatic.values_list('beneficiarios_cargados',flat=True).distinct().count()
        kwargs['evidencias_escuelatic_r2'] = evidencias_r2_escuelatic.count()

        kwargs['ple_r1'] = ple_r1.count()
        kwargs['ple_r2'] = ple_r2.count()

        return super(NuevoRedView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()

        red = Red.objects.get(id = self.object.id)

        if not red.producto_final:
            evidencias = Evidencia.objects.filter(red_id = None)

            region_1 = Region.objects.get(numero = 1)
            region_2 = Region.objects.get(numero = 2)

            evidencias_r1 = evidencias.filter(formador__region = region_1)
            evidencias_r2 = evidencias.filter(formador__region = region_2)

            evidencias_r1_innovatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
            evidencias_r1_tecnotic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
            evidencias_r1_directic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
            evidencias_r1_escuelatic = evidencias_r1.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')

            evidencias_r2_innovatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'INNOVATIC')
            evidencias_r2_tecnotic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'TECNOTIC')
            evidencias_r2_directic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'DIRECTIC')
            evidencias_r2_escuelatic = evidencias_r2.filter(entregable__sesion__nivel__diplomado__nombre = 'ESCUELA TIC FAMILIA')



            if self.object.region.numero == 1:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    evidencias_r1_innovatic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'TECNOTIC':
                    evidencias_r1_tecnotic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'DIRECTIC':
                    evidencias_r1_directic.update(red_id = red.id)
                elif self.object.diplomado.nombre == 'ESCUELA TIC FAMILIA':
                    evidencias_r1_escuelatic.update(red_id = red.id)
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
                else:
                    pass


            else:
                pass
            red.save()
            build_red.delay(red.id)
        else:
            ple_r1 = Beneficiario.objects.filter(region__id=1, estado_producto_final='cargado')
            ple_r2 = Beneficiario.objects.filter(region__id=2, estado_producto_final='cargado')

            if self.object.region.numero == 1:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    for beneficiario in ple_r1:
                        red.beneficiarios.add(beneficiario)
                        beneficiario.estado_producto_final = 'enviado'
                        beneficiario.save()
                else:
                    pass

            elif self.object.region.numero == 2:
                if self.object.diplomado.nombre == 'INNOVATIC':
                    for beneficiario in ple_r2:
                        red.beneficiarios.add(beneficiario)
                        beneficiario.estado_producto_final = 'enviado'
                        beneficiario.save()
                else:
                    pass

            else:
                pass

            red.save()
            build_red_producto_final.delay(red.id)
        return HttpResponseRedirect(self.get_success_url())


class UpdateRedView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Red
    form_class = RedRetroalimentacionForm
    success_url = '../../'
    template_name = 'evidencias/red/editar.html'
    permission_required = "permisos_sican.evidencias.red.editar"


    def form_valid(self, form):
        self.object = form.save()
        retroalimentacion_red.delay(self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class CargaMasivaListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/cargamasiva/lista.html'
    permission_required = "permisos_sican.evidencias.cargamasivaevidencias.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.evidencias.cargamasivaevidencias.crear')
        return super(CargaMasivaListView,self).get_context_data(**kwargs)


class NuevoCargaMasivaView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = CargaMasiva
    form_class = CargaMasivaForm
    success_url = '../'
    template_name = 'evidencias/cargamasiva/nuevo.html'
    permission_required = "permisos_sican.evidencias.cargamasivaevidencias.crear"

    def get_initial(self):
        return {'id_usuario':self.request.user.id}

    def form_valid(self, form):
        self.object = form.save()
        carga_masiva_evidencias.delay(self.object.id,self.request.user.id)
        return super(NuevoCargaMasivaView,self).form_valid(form)


class AuxiliaresListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/rendimiento/lista.html'
    permission_required = "permisos_sican.auxiliares.rendimiento.ver"


class BeneficiarioEvidenciaCedulaList(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/cedula/lista_beneficiarios.html'
    permission_required = "permisos_sican.evidencias.cedula_beneficiario.ver"


class BeneficiarioEvidenciaCedulaProductoList(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/cedula/lista_productos.html'
    permission_required = "permisos_sican.evidencias.cedula_beneficiario.ver"


    def get_context_data(self, **kwargs):
        kwargs['id_beneficiario'] = self.kwargs['id_beneficiario']
        kwargs['nombre_beneficiario'] = Beneficiario.objects.get(id = self.kwargs['id_beneficiario']).get_full_name()
        return super(BeneficiarioEvidenciaCedulaProductoList,self).get_context_data(**kwargs)

class SubsanacionListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/subsanacion/lista_reds.html'
    permission_required = "permisos_sican.evidencias.subsanacion.ver"


class SubsanacionEvidenciasListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/subsanacion/lista_evidencias.html'
    permission_required = "permisos_sican.evidencias.subsanacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['id_red'] = self.kwargs['id_red']
        return super(SubsanacionEvidenciasListView,self).get_context_data(**kwargs)



class PleListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/ple/lista.html'
    permission_required = "permisos_sican.evidencias.subsanacion_ple.ver"






class PleBeneficiarioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):
    form_class = PleBeneficiarioForm
    success_url = '../../'
    template_name = 'evidencias/ple/editar.html'
    permission_required = "permisos_sican.evidencias.subsanacion_ple.editar"


    def get_context_data(self, **kwargs):
        kwargs['cedula'] = Beneficiario.objects.get(id=self.kwargs['id_beneficiario']).cedula
        return super(PleBeneficiarioView,self).get_context_data(**kwargs)

    def get_initial(self):
        return {'beneficiario':Beneficiario.objects.get(id=self.kwargs['id_beneficiario'])}


    def form_valid(self, form):
        beneficiario = Beneficiario.objects.get(id=self.kwargs['id_beneficiario'])


        beneficiario.nombre_producto_final = form.cleaned_data['nombre']
        beneficiario.area_basica_producto_final = form.cleaned_data['area']
        beneficiario.estado_producto_final = 'cargado'
        beneficiario.para_leer = form.cleaned_data['para_leer']
        beneficiario.para_hacer_1 = form.cleaned_data['para_hacer_1']
        beneficiario.para_hacer_2 = form.cleaned_data['para_hacer_2']
        beneficiario.para_hacer_3 = form.cleaned_data['para_hacer_3']
        beneficiario.para_hacer_4 = form.cleaned_data['para_hacer_4']
        beneficiario.imagen_historieta = form.cleaned_data['imagen_historieta']
        beneficiario.imagen_infografia = form.cleaned_data['imagen_infografia']
        beneficiario.imagen_graficacion_ple = form.cleaned_data['imagen_graficacion_ple']
        beneficiario.link_ruta_sostenibilidad = form.cleaned_data['link_ruta_sostenibilidad']
        beneficiario.imagen_para_leer = form.cleaned_data['imagen_para_leer']
        beneficiario.html = File(open(settings.STATICFILES_DIRS[0] + '\\documentos\\ple.html'))
        beneficiario.save()

        file = codecs.open(beneficiario.html.path, 'r+', 'utf-8')
        text_index_1 = file.read()
        file = codecs.open(beneficiario.html.path, 'w', 'utf-8')

        para_hacer_adicionales = []

        if beneficiario.para_hacer_2 != "":
            para_hacer_adicionales.append(beneficiario.para_hacer_2)

        if beneficiario.para_hacer_3 != "":
            para_hacer_adicionales.append(beneficiario.para_hacer_3)

        if beneficiario.para_hacer_4 != "":
            para_hacer_adicionales.append(beneficiario.para_hacer_4)


        adicional = ''

        for x in para_hacer_adicionales:
            adicional += '<div class="col-lg-12" style="margin-bottom: 50px;"><iframe style="width: 82vw;height: 100vh;position: relative;" src="'+x+'" frameborder="0" allowfullscreen></iframe></div>'


        navar_color_list = ['#194F83','#4C4A9C',"#831A1C","#008346"]
        section_color_list = ['#3DCF8C',"#3DC8CF","#9C9671","#9C3DCF"]

        navar_color = random.choice(navar_color_list)
        section_color = random.choice(section_color_list)

        imagen_para_leer = ''
        if beneficiario.imagen_para_leer != None:
            imagen_para_leer = '<img src="' + beneficiario.imagen_para_leer.url + '" class="img-responsive center-block">'

        file.write(text_index_1.replace('{{IMAGEN_PARA_LEER}}',imagen_para_leer).replace('{{NAVAR_COLOR}}',navar_color).replace('{{SECTION_COLOR}}',section_color).replace('{{TITULO}}', beneficiario.nombre_producto_final).replace('{{NOMBRE_DOCENTE}}',beneficiario.nombres+" "+beneficiario.apellidos + " - "+str(beneficiario.cedula)).replace('{{TEXTO_PARA_LEER}}',beneficiario.para_leer).replace('{{URL_PARA_HACER}}',beneficiario.para_hacer_1).replace('{{URL_PARA_HACER_ADICIONAL}}',adicional).replace('{{URL_HISTORIETA}}',beneficiario.imagen_historieta.url).replace('{{URL_INFOGRAFIA}}',beneficiario.imagen_infografia.url).replace('{{URL_GRAFICACION_PLE}}',beneficiario.imagen_graficacion_ple.url).replace('{{URL_RUTA_SOSTENIBILIDAD}}',beneficiario.link_ruta_sostenibilidad.replace('scene','card')))

        file.close()

        beneficiario.link = beneficiario.html.url

        beneficiario.save()


        return HttpResponseRedirect(self.get_success_url())





class SubsanacionEvidenciasFormView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):

    form_class = SubsanacionEvidenciaForm
    success_url = '../'
    template_name = 'evidencias/subsanacion/evidencia.html'
    permission_required = "permisos_sican.evidencias.subsanacion.crear"

    def get_context_data(self, **kwargs):

        evidencia = Evidencia.objects.get(id = self.kwargs['id_evidencia'])

        kwargs['id_red'] = self.kwargs['id_red']
        kwargs['id_evidencia'] = self.kwargs['id_evidencia']
        kwargs['link_soporte'] = evidencia.get_archivo_url()
        kwargs['nombre_soporte'] = os.path.basename(evidencia.archivo.name)

        return super(SubsanacionEvidenciasFormView,self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_red':self.kwargs['id_red'],'id_evidencia':self.kwargs['id_evidencia']}

    def form_valid(self, form):
        keys = list(form.cleaned_data.keys())
        keys.remove('archivo')
        keys.remove('observacion')

        evidencia = Evidencia.objects.get(id = self.kwargs['id_evidencia'])


        if form.cleaned_data['archivo'] != None:
            archivo = form.cleaned_data['archivo']
        else:
            archivo = evidencia.archivo

        nueva_evidencia = Evidencia.objects.create(usuario = self.request.user,archivo = archivo,entregable=evidencia.entregable,
                                                   formador=evidencia.formador,subsanacion=True)

        cantidad = 0

        for key in keys:
            if form.cleaned_data[key]:
                cantidad += 1
                beneficiario = Beneficiario.objects.get(id = key.split('_')[1])
                nueva_evidencia.beneficiarios_cargados.add(beneficiario)
                rechazo = Rechazo.objects.filter(evidencia_id__exact = self.kwargs['id_evidencia'],beneficiario_rechazo = beneficiario)

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
                                   red = Red.objects.get(id = self.kwargs['id_red']),observacion = form.cleaned_data['observacion'])


        return super(SubsanacionEvidenciasFormView,self).form_valid(form)




class SubsanacionEvidenciasBeneficiarioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):

    model = Beneficiario
    form_class = BeneficiarioUpdateForm
    success_url = '../../'
    template_name = 'evidencias/subsanacion/actualizar_participante.html'
    permission_required = "permisos_sican.evidencias.subsanacion.crear"
    pk_url_kwarg = 'id_beneficiario'

    def get_context_data(self, **kwargs):

        evidencia = Evidencia.objects.get(id = self.kwargs['id_evidencia'])

        kwargs['id_red'] = self.kwargs['id_red']
        kwargs['id_evidencia'] = self.kwargs['id_evidencia']
        kwargs['link_soporte'] = evidencia.get_archivo_url()
        kwargs['nombre_soporte'] = os.path.basename(evidencia.archivo.name)

        return super(SubsanacionEvidenciasBeneficiarioView,self).get_context_data(**kwargs)


    def get_initial(self):
        return {'id_red':self.kwargs['id_red'],'id_evidencia':self.kwargs['id_evidencia'],'diplomado_nombre':self.object.diplomado.nombre.upper(),'formador_id':self.object.formador.id,'beneficiario_id':self.object.id}


    def form_valid(self, form):
        self.object = form.save()
        if self.object.diplomado.nombre != 'ESCUELA TIC FAMILIA':
            self.object.radicado = Radicado.objects.get(numero=form.cleaned_data['radicado_text'])
        self.object.save()
        return super(SubsanacionEvidenciasBeneficiarioView, self).form_valid(form)




class ListaSubsanacionEvidenciaView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'evidencias/subsanacion/lista_subsanaciones.html'
    permission_required = "permisos_sican.evidencias.subsanacion.ver"

    def get_context_data(self, **kwargs):

        evidencia = Evidencia.objects.get(id = self.kwargs['id_evidencia'])

        kwargs['id_red'] = self.kwargs['id_red']
        kwargs['id_evidencia'] = self.kwargs['id_evidencia']
        kwargs['link_soporte'] = evidencia.get_archivo_url()
        kwargs['nombre_soporte'] = os.path.basename(evidencia.archivo.name)

        return super(ListaSubsanacionEvidenciaView,self).get_context_data(**kwargs)