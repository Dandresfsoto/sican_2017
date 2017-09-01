#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from preinscripcion.models import DocentesPreinscritos
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from administrativos.forms import NuevoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from preinscripcion.forms import DocentesPreinscritosForm, DocentesPreinscritosUpdateForm
from docentes.models import DocentesMinEducacion
from formadores.models import Formador
from formadores.models import SolicitudTransporte
from formadores.forms import SolicitudTransporteLiderForm, SolicitudTransporteUpdateForm
from municipios.models import Municipio
from departamentos.models import Departamento
from formadores.models import SolicitudTransporte, Desplazamiento
from django.views.generic.edit import ModelFormMixin
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL,RECURSO_HUMANO_EMAIL
import locale
from formacion.models import Semana
import datetime
from isoweek import Week
from formacion.models import EntradaCronograma
from formacion.forms import EntradaCronogramaform, EntradaCronogramaUpdateform
from productos.models import Nivel, Actividades
from formacion.models import Grupos
from formadores.forms import GruposForm, RevisionForm, RevisionUpdateForm
from formadores.models import Revision
from productos.models import Contratos, ValorEntregable
from formadores.models import Producto, Revision
from rh.models import RequerimientoPersonal
from rh.forms import RequerimientoPersonalForm, RequerimientoPersonalRhCapacitado
from django.utils import timezone
from cargos.models import Cargo



class DiplomasEscuelaTic(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/diplomas/escuelatic/lista.html'
    permission_required = "permisos_sican.formacion.diplomas.ver"

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.formacion.diplomas.informes')
        return super(DiplomasEscuelaTic, self).get_context_data(**kwargs)

class ListaPreinscritosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/preinscritos/lista.html'
    permission_required = "permisos_sican.formacion.preinscritos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.preinscritos.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.formacion.preinscritos.informes')
        return super(ListaPreinscritosView, self).get_context_data(**kwargs)

class NuevoPreinscritoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = DocentesPreinscritos
    form_class = DocentesPreinscritosForm
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/nuevo.html'
    permission_required = "permisos_sican.formacion.preinscritos.crear"


    def form_valid(self, form):
        self.object = form.save()
        try:
            docente = DocentesMinEducacion.objects.get(cedula=self.object.cedula)
        except:
            pass
        else:
            self.object.verificado = True
            self.object.save()
        return super(NuevoPreinscritoView,self).form_valid(form)

class UpdatePreinscritoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = DocentesPreinscritos
    form_class = DocentesPreinscritosUpdateForm
    pk_url_kwarg = 'pk'
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/editar.html'
    permission_required = "permisos_sican.formacion.preinscritos.editar"

    def get_initial(self):
        return {'departamento':self.object.departamento.id,'municipio':self.object.municipio.id}

    def form_valid(self, form):
        self.object = form.save()
        try:
            docente = DocentesMinEducacion.objects.get(cedula=self.object.cedula)
        except:
            pass
        else:
            self.object.verificado = True
            self.object.save()
        return super(UpdatePreinscritoView,self).form_valid(form)

class DeletePreinscritoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = DocentesPreinscritos
    pk_url_kwarg = 'pk'
    success_url = '/formacion/preinscritos/'
    template_name = 'formacion/preinscritos/eliminar.html'
    permission_required = "permisos_sican.formacion.preinscritos.eliminar"




class ListaTransportesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"


class ListaTransportesConsignadasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/consignadas/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesConsignadasView,self).get_context_data(**kwargs)


class ListaTransportesAprobadasFinancieraView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/aprobadasfinanciera/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesAprobadasFinancieraView,self).get_context_data(**kwargs)

class ListaTransportesAprobadasLideresView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/aprobadaslideres/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesAprobadasLideresView,self).get_context_data(**kwargs)


class ListaTransportesRechazadasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/rechazadas/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesRechazadasView,self).get_context_data(**kwargs)


class ListaTransportesPendientesView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/transportes/pendientes/lista.html'
    permission_required = "permisos_sican.formacion.transportesformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id'])
        kwargs['formador_id'] = self.kwargs['id']
        return super(ListaTransportesPendientesView,self).get_context_data(**kwargs)

class TransporteFormView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = SolicitudTransporte
    form_class = SolicitudTransporteLiderForm
    pk_url_kwarg = 'id_solicitud'
    success_url = '../../'
    template_name = 'formacion/transportes/pendientes/estado.html'
    permission_required = "permisos_sican.formacion.transportesformacion.estado"

    def form_valid(self, form):
        self.object.aprobacion_lider = timezone.localtime(timezone.now())
        self.object = form.save()
        valores = self.object.desplazamientos.all().values_list('valor',flat=True)
        valor_aprobado = 0

        for valor in valores:
            valor_aprobado += valor

        if self.object.estado == 'aprobado_lider':
            self.object.valor_aprobado_lider = valor_aprobado
            self.object.save()

        elif self.object.estado == 'rechazado':
            self.object.valor_aprobado_lider = 0
            self.object.save()
            send_mail_templated.delay('email/desplazamiento.tpl',
                                      {
                                          'url_base':'http://sican.asoandes.org/',
                                          'fullname':self.object.formador.get_full_name(),
                                          'nombre_solicitud': self.object.nombre,
                                          'fecha_solicitud': self.object.creacion.strftime('%d/%m/%Y'),
                                          'valor_solicitado': locale.currency(self.object.valor,grouping=True),
                                          'valor_aprobado': locale.currency(valor_aprobado,grouping=True),
                                          'observacion': form.cleaned_data['observacion'],
                                          'estado': 'Solicitud rechazada'
                                      },
                                      DEFAULT_FROM_EMAIL, [self.object.formador.correo_personal])

        else:
            self.object.valor_aprobado_lider = 0
            self.object.save()

        return super(ModelFormMixin,self).form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['formador'] = self.object.formador.get_full_name()
        kwargs['valor'] = locale.currency( self.object.valor, grouping=True ).replace('+','')
        return super(TransporteFormView,self).get_context_data(**kwargs)



class TransporteFormUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               FormView):
    form_class = SolicitudTransporteUpdateForm
    success_url = '../../'
    template_name = 'formacion/transportes/pendientes/editar.html'
    permission_required = "permisos_sican.formacion.transportesformacion.editar"

    def get_initial(self):
        return {'pk':self.kwargs['id_solicitud']}

    def get_context_data(self, **kwargs):
        solicitud = SolicitudTransporte.objects.get(id=self.kwargs['id_solicitud'])
        kwargs['formador'] = Formador.objects.get(id = solicitud.formador.id).get_full_name()
        kwargs['nombre_solicitud'] = solicitud.nombre
        return super(TransporteFormUpdateView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        desplazamientos = [
            {
                'id':form.cleaned_data['id_1'],
                'fecha':form.cleaned_data['fecha_1'],
                'd_origen':form.cleaned_data['departamento_origen_1'],
                'm_origen':form.cleaned_data['municipio_origen_1'],
                'd_destino':form.cleaned_data['departamento_destino_1'],
                'm_destino':form.cleaned_data['municipio_destino_1'],
                'valor':float(form.cleaned_data['valor_1'].replace(',','')) if form.cleaned_data['valor_1'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_1'],
            },
            {
                'id':form.cleaned_data['id_2'],
                'fecha':form.cleaned_data['fecha_2'],
                'd_origen':form.cleaned_data['departamento_origen_2'],
                'm_origen':form.cleaned_data['municipio_origen_2'],
                'd_destino':form.cleaned_data['departamento_destino_2'],
                'm_destino':form.cleaned_data['municipio_destino_2'],
                'valor':float(form.cleaned_data['valor_2'].replace(',','')) if form.cleaned_data['valor_2'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_2'],
            },
            {
                'id':form.cleaned_data['id_3'],
                'fecha':form.cleaned_data['fecha_3'],
                'd_origen':form.cleaned_data['departamento_origen_3'],
                'm_origen':form.cleaned_data['municipio_origen_3'],
                'd_destino':form.cleaned_data['departamento_destino_3'],
                'm_destino':form.cleaned_data['municipio_destino_3'],
                'valor':float(form.cleaned_data['valor_3'].replace(',','')) if form.cleaned_data['valor_3'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_3'],
            },
            {
                'id':form.cleaned_data['id_4'],
                'fecha':form.cleaned_data['fecha_4'],
                'd_origen':form.cleaned_data['departamento_origen_4'],
                'm_origen':form.cleaned_data['municipio_origen_4'],
                'd_destino':form.cleaned_data['departamento_destino_4'],
                'm_destino':form.cleaned_data['municipio_destino_4'],
                'valor':float(form.cleaned_data['valor_4'].replace(',','')) if form.cleaned_data['valor_4'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_4'],
            },
            {
                'id':form.cleaned_data['id_5'],
                'fecha':form.cleaned_data['fecha_5'],
                'd_origen':form.cleaned_data['departamento_origen_5'],
                'm_origen':form.cleaned_data['municipio_origen_5'],
                'd_destino':form.cleaned_data['departamento_destino_5'],
                'm_destino':form.cleaned_data['municipio_destino_5'],
                'valor':float(form.cleaned_data['valor_5'].replace(',','')) if form.cleaned_data['valor_5'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_5'],
            },
            {
                'id':form.cleaned_data['id_6'],
                'fecha':form.cleaned_data['fecha_6'],
                'd_origen':form.cleaned_data['departamento_origen_6'],
                'm_origen':form.cleaned_data['municipio_origen_6'],
                'd_destino':form.cleaned_data['departamento_destino_6'],
                'm_destino':form.cleaned_data['municipio_destino_6'],
                'valor':float(form.cleaned_data['valor_6'].replace(',','')) if form.cleaned_data['valor_6'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_6'],
            },
            {
                'id':form.cleaned_data['id_7'],
                'fecha':form.cleaned_data['fecha_7'],
                'd_origen':form.cleaned_data['departamento_origen_7'],
                'm_origen':form.cleaned_data['municipio_origen_7'],
                'd_destino':form.cleaned_data['departamento_destino_7'],
                'm_destino':form.cleaned_data['municipio_destino_7'],
                'valor':float(form.cleaned_data['valor_7'].replace(',','')) if form.cleaned_data['valor_7'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_7'],
            },
            {
                'id':form.cleaned_data['id_8'],
                'fecha':form.cleaned_data['fecha_8'],
                'd_origen':form.cleaned_data['departamento_origen_8'],
                'm_origen':form.cleaned_data['municipio_origen_8'],
                'd_destino':form.cleaned_data['departamento_destino_8'],
                'm_destino':form.cleaned_data['municipio_destino_8'],
                'valor':float(form.cleaned_data['valor_8'].replace(',','')) if form.cleaned_data['valor_8'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_8'],
            },
            {
                'id':form.cleaned_data['id_9'],
                'fecha':form.cleaned_data['fecha_9'],
                'd_origen':form.cleaned_data['departamento_origen_9'],
                'm_origen':form.cleaned_data['municipio_origen_9'],
                'd_destino':form.cleaned_data['departamento_destino_9'],
                'm_destino':form.cleaned_data['municipio_destino_9'],
                'valor':float(form.cleaned_data['valor_9'].replace(',','')) if form.cleaned_data['valor_9'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_9'],
            },
            {
                'id':form.cleaned_data['id_10'],
                'fecha':form.cleaned_data['fecha_10'],
                'd_origen':form.cleaned_data['departamento_origen_10'],
                'm_origen':form.cleaned_data['municipio_origen_10'],
                'd_destino':form.cleaned_data['departamento_destino_10'],
                'm_destino':form.cleaned_data['municipio_destino_10'],
                'valor':float(form.cleaned_data['valor_10'].replace(',','')) if form.cleaned_data['valor_10'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_10'],
            },
        ]

        valor = 0

        for desplazamiento in desplazamientos:
            if desplazamiento['id'] != '':
                if desplazamiento['valor'] != None:
                    if desplazamiento['fecha'] != '':
                        if desplazamiento['d_origen'] != '':
                            if desplazamiento['m_origen'] != '':
                                if desplazamiento['d_destino'] != '':
                                    if desplazamiento['m_destino'] != '':
                                        if desplazamiento['motivo'] != '':
                                            valor += desplazamiento['valor']
                                            editar = Desplazamiento.objects.get(id=desplazamiento['id'])
                                            editar.departamento_origen = Departamento.objects.get(id=desplazamiento['d_origen'])
                                            editar.municipio_origen = Municipio.objects.get(id=desplazamiento['m_origen'])
                                            editar.departamento_destino = Departamento.objects.get(id=desplazamiento['d_destino'])
                                            editar.municipio_destino = Municipio.objects.get(id=desplazamiento['m_destino'])
                                            editar.valor = desplazamiento['valor']
                                            editar.fecha = desplazamiento['fecha']
                                            editar.motivo = desplazamiento['motivo']
                                            editar.save()

        solicitud = SolicitudTransporte.objects.get(id=self.kwargs['id_solicitud'])
        solicitud.valor_aprobado_lider = valor
        solicitud.observacion = 'Se modificaron los valores de desplazamiento por el lider'
        solicitud.save()



        return super(TransporteFormUpdateView,self).form_valid(form)


class ListaCronogramasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/cronograma/semanas.html'
    permission_required = "permisos_sican.formacion.cronograma.ver"

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.formacion.cronograma.informes')
        return super(ListaCronogramasView,self).get_context_data(**kwargs)



class ListaCronogramasSemanaView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/cronograma/lista.html'
    permission_required = "permisos_sican.formacion.cronograma.ver"

    def get_context_data(self, **kwargs):
        semana = Semana.objects.get(id=self.kwargs['semana_id'])
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.formacion.cronograma.informes')
        kwargs['numero_semana'] = Semana.objects.get(id=self.kwargs['semana_id']).numero
        kwargs['id_semana'] = self.kwargs['semana_id']

        inicio = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).monday()
        fin = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).sunday()

        kwargs['fechas'] = inicio.strftime("%d de %B del %Y") + ' - ' + fin.strftime("%d de %B del %Y")

        return super(ListaCronogramasSemanaView,self).get_context_data(**kwargs)



class CronogramaFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/cronograma/cronograma.html'
    permission_required = "permisos_sican.formacion.cronograma.editar"


    def get_context_data(self, **kwargs):
        semana = Semana.objects.get(id=self.kwargs['semana_id'])
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id']).get_full_name()
        kwargs['semana_numero'] = semana.numero
        kwargs['id_semana'] = semana.id

        x, created = Semana.objects.get_or_create(numero = datetime.datetime.now().isocalendar()[1]+1)

        inicio = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).monday()
        fin = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).sunday()

        kwargs['fechas'] = inicio.strftime("%d de %B del %Y") + ' - ' + fin.strftime("%d de %B del %Y")
        kwargs['id_formador'] = self.kwargs['id']

        return super(CronogramaFormadorView,self).get_context_data(**kwargs)


class CronogramaFormadorNuevoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = EntradaCronograma
    form_class = EntradaCronogramaform
    success_url = '../'
    template_name = 'formacion/cronograma/nuevo.html'
    permission_required = "permisos_sican.formacion.cronograma.crear"

    def get_initial(self):
        return {'formador':self.kwargs['id'],'semana':self.kwargs['semana_id']}

    def get_context_data(self, **kwargs):
        semana = Semana.objects.get(id=self.kwargs['semana_id'])

        inicio = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).tuesday()
        fin = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+2).monday()

        kwargs['start_date'] = inicio.strftime("%Y-%m-%d")
        kwargs['end_date'] = fin.strftime("%Y-%m-%d")
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id']).get_full_name()
        kwargs['numero_semana'] = semana.numero
        return super(CronogramaFormadorNuevoView,self).get_context_data(**kwargs)


    def form_valid(self, form):
        semana = form.cleaned_data['semana']
        formador = form.cleaned_data['formador']
        departamento = form.cleaned_data['departamento']
        municipio = form.cleaned_data['municipio']
        secretaria = form.cleaned_data['secretaria']
        grupo = form.cleaned_data['grupo']
        numero_sedes = form.cleaned_data['numero_sedes']

        actividades = form.cleaned_data['actividades_entrada']
        beneficiados = form.cleaned_data['beneficiados']
        fecha = form.cleaned_data['fecha']
        institucion = form.cleaned_data['institucion']
        direccion = form.cleaned_data['direccion']
        telefono = form.cleaned_data['telefono']
        hora_inicio = form.cleaned_data['hora_inicio']

        ubicacion = form.cleaned_data['ubicacion']
        observaciones = form.cleaned_data['observaciones']

        niveles_id = []
        delta = 0

        for actividad in actividades:
            delta += actividad.horas
            if actividad.sesion.nivel.id not in niveles_id:
                niveles_id.append(actividad.sesion.nivel.id)

        hora_finalizacion = datetime.time(hora_inicio.hour+delta,hora_inicio.minute,hora_inicio.second)
        x = 0

        self.object = EntradaCronograma(semana = semana,
                                        formador = formador,
                                        departamento = departamento,
                                        municipio = municipio,
                                        secretaria = secretaria,
                                        grupo = grupo,
                                        numero_sedes = numero_sedes,
                                        beneficiados = beneficiados,
                                        fecha = fecha,
                                        institucion = institucion,
                                        direccion = direccion,
                                        telefono = telefono,
                                        hora_inicio = hora_inicio,
                                        hora_finalizacion = hora_finalizacion,
                                        ubicacion = ubicacion,
                                        observaciones = observaciones
                                        )
        self.object.save()
        for actividad in actividades:
            self.object.actividades_entrada.add(actividad)

        for nivel in Nivel.objects.filter(id__in = niveles_id):
            self.object.nivel.add(nivel)

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CronogramaFormadorUpdateView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = EntradaCronograma
    form_class = EntradaCronogramaUpdateform
    success_url = '../../'
    pk_url_kwarg = 'id_entrada'
    template_name = 'formacion/cronograma/editar.html'
    permission_required = "permisos_sican.formacion.cronograma.editar"

    def get_initial(self):
        return {'formador':self.kwargs['id'],'id':self.object.id,'semana':self.kwargs['semana_id'],'fecha':self.object.fecha}

    def get_context_data(self, **kwargs):
        semana = Semana.objects.get(id=self.kwargs['semana_id'])

        inicio = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+1).tuesday()
        fin = Week(semana.creacion.isocalendar()[0],semana.creacion.isocalendar()[1]+2).monday()

        kwargs['start_date'] = inicio.strftime("%Y-%m-%d")
        kwargs['end_date'] = fin.strftime("%Y-%m-%d")
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id']).get_full_name()
        kwargs['numero_semana'] = semana.numero
        return super(CronogramaFormadorUpdateView,self).get_context_data(**kwargs)


    def form_valid(self, form):
        semana = form.cleaned_data['semana']
        formador = form.cleaned_data['formador']
        departamento = form.cleaned_data['departamento']
        municipio = form.cleaned_data['municipio']
        secretaria = form.cleaned_data['secretaria']
        grupo = form.cleaned_data['grupo']
        numero_sedes = form.cleaned_data['numero_sedes']

        actividades = form.cleaned_data['actividades_entrada']
        beneficiados = form.cleaned_data['beneficiados']
        fecha = form.cleaned_data['fecha']
        institucion = form.cleaned_data['institucion']
        direccion = form.cleaned_data['direccion']
        telefono = form.cleaned_data['telefono']
        hora_inicio = form.cleaned_data['hora_inicio']

        ubicacion = form.cleaned_data['ubicacion']
        observaciones = form.cleaned_data['observaciones']

        niveles_id = []
        delta = 0

        for actividad in actividades:
            delta += actividad.horas
            if actividad.sesion.nivel.id not in niveles_id:
                niveles_id.append(actividad.sesion.nivel.id)

        hora_finalizacion = datetime.time(hora_inicio.hour+delta,hora_inicio.minute,hora_inicio.second)
        x = self.object
        x.actividades_entrada.clear()
        x.nivel.clear()
        x.semana = semana
        x.formador = formador
        x.departamento = departamento
        x.municipio = municipio
        x.secretaria = secretaria
        x.grupo = grupo
        x.numero_sedes = numero_sedes
        x.beneficiados = beneficiados
        x.fecha = fecha
        x.institucion = institucion
        x.direccion = direccion
        x.telefono = telefono
        x.hora_inicio = hora_inicio
        x.hora_finalizacion = hora_finalizacion
        x.ubicacion = ubicacion
        x.observaciones = observaciones
        x.save()

        for actividad in actividades:
            x.actividades_entrada.add(actividad)

        for nivel in Nivel.objects.filter(id__in = niveles_id):
            x.nivel.add(nivel)

        x.save()

        return HttpResponseRedirect(self.get_success_url())


class CronogramaFormadorDeleteView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = EntradaCronograma
    pk_url_kwarg = 'id_entrada'
    success_url = '../../'
    template_name = 'formacion/cronograma/eliminar.html'
    permission_required = "permisos_sican.formacion.cronograma.eliminar"


class ListadoFormadoresGruposView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/grupos/lista_formadores.html'
    permission_required = "permisos_sican.formacion.gruposformacion.ver"


class FormadoresGruposLista(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/grupos/lista_grupos.html'
    permission_required = "permisos_sican.formacion.gruposformacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['formador_id'] = self.kwargs['id_formador']
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.gruposformacion.crear')
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        return super(FormadoresGruposLista,self).get_context_data(**kwargs)


class NuevoGrupoFormador(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Grupos
    form_class = GruposForm
    success_url = './'
    template_name = 'formacion/grupos/nuevo.html'
    permission_required = "permisos_sican.formacion.gruposformacion.crear"

    def get_initial(self):
        return {'formador_id':self.kwargs['id_formador']}

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        return super(NuevoGrupoFormador,self).get_context_data(**kwargs)


class EditarGrupoFormador(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Grupos
    form_class = GruposForm
    success_url = '../../'
    pk_url_kwarg = 'id_grupo'
    template_name = 'formacion/grupos/editar.html'
    permission_required = "permisos_sican.formacion.gruposformacion.editar"

    def get_initial(self):
        return {'formador_id':self.kwargs['id_formador']}

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        return super(EditarGrupoFormador,self).get_context_data(**kwargs)


class EliminarGrupoFormador(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Grupos
    pk_url_kwarg = 'id_grupo'
    success_url = '../../'
    template_name = 'formacion/grupos/eliminar.html'
    permission_required = "permisos_sican.formacion.gruposformacion.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        return super(EliminarGrupoFormador,self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)





class ListaRevisionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/revision/lista.html'
    permission_required = "permisos_sican.formacion.revision.ver"

    def get_context_data(self, **kwargs):
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.revision.informes')
        return super(ListaRevisionView, self).get_context_data(**kwargs)



class ListaRevisionFormadorView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/revision/lista_revisiones.html'
    permission_required = "permisos_sican.formacion.revision.ver"


    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.revision.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.revision.informes')
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['id_cargo'] = self.kwargs['id_cargo']
        kwargs['nombre_cargo'] = Cargo.objects.get(id = self.kwargs['id_cargo']).nombre
        return super(ListaRevisionFormadorView, self).get_context_data(**kwargs)




class ListaRevisionTipologiaView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/revision/lista_revisiones_diplomado.html'
    permission_required = "permisos_sican.formacion.revision.ver"


    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.revision.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.revision.informes')
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        return super(ListaRevisionTipologiaView, self).get_context_data(**kwargs)





class NuevaRevisionFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Revision
    form_class = RevisionForm
    success_url = '../'
    template_name = 'formacion/revision/nuevo.html'
    permission_required = "permisos_sican.formacion.revision.crear"

    def get_initial(self):
        return {'formador_id':self.kwargs['id_formador'],'cargo_id':self.kwargs['id_cargo']}

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        kwargs['id_cargo'] = self.kwargs['id_cargo']
        kwargs['nombre_cargo'] = Cargo.objects.get(id = self.kwargs['id_cargo']).nombre
        return super(NuevaRevisionFormadorView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        formador = Formador.objects.get(id = self.kwargs['id_formador'])

        cargo = Cargo.objects.get(id = self.kwargs['id_cargo'])

        contrato = Contratos.objects.filter(cargo = cargo).get(nombre = 'Capacitación 1') if formador.primera_capacitacion else Contratos.objects.filter(cargo = cargo).get(nombre = 'Capacitación 2')
        entregables = ValorEntregable.objects.filter(contrato = contrato)

        for entregable in entregables:
            producto = Producto.objects.create(valor_entregable = entregable,cantidad = form.cleaned_data['field_'+str(entregable.entregable.id)])
            self.object.productos.add(producto)

        return super(NuevaRevisionFormadorView,self).form_valid(form)


class EditarRevisionFormadorView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Revision
    form_class = RevisionUpdateForm
    pk_url_kwarg = 'id_revision'
    success_url = '../../'
    template_name = 'formacion/revision/editar.html'
    permission_required = "permisos_sican.formacion.revision.editar"

    def get_initial(self):
        return {'id':self.kwargs['id_revision']}

    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id=self.kwargs['id_formador']).get_full_name()
        return super(EditarRevisionFormadorView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        revision_object = Revision.objects.get(id = self.kwargs['id_revision'])

        for producto in revision_object.productos.all():
            entregable = producto.valor_entregable
            producto = Producto.objects.get(id=producto.id)
            producto.cantidad = form.cleaned_data['field_'+str(entregable.entregable.id)]
            producto.save()

        return super(EditarRevisionFormadorView,self).form_valid(form)


class ListaRequerimientosContratacionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'formacion/requerimientosrh/lista.html'
    permission_required = "permisos_sican.formacion.requerimientosrh.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.formacion.requerimientosrh.crear')
        return super(ListaRequerimientosContratacionView, self).get_context_data(**kwargs)




class NuevoRequerimientoContratacionView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = RequerimientoPersonal
    form_class = RequerimientoPersonalForm
    success_url = '../'
    template_name = 'formacion/requerimientosrh/nuevo.html'
    permission_required = "permisos_sican.formacion.requerimientosrh.crear"

    def get_initial(self):
        return {'user_id':self.request.user.id}



class UpdateRequerimientoContratacionView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = RequerimientoPersonal
    form_class = RequerimientoPersonalRhCapacitado
    pk_url_kwarg = 'pk'
    success_url = '/formacion/requerimientoscontratacion/'
    template_name = 'formacion/requerimientosrh/editar.html'
    permission_required = "permisos_sican.formacion.requerimientosrh.editar"

    def form_valid(self, form):
        self.object = form.save()
        self.object.remitido_contratacion = True
        self.object.fecha_solicitud_contratacion = datetime.datetime.now()
        if form.cleaned_data['contratar'] == 'contratar':
            self.object.contratar = True
        elif form.cleaned_data['contratar'] == 'desierto':
            self.object.desierto = True
        self.object.save()
        return super(UpdateRequerimientoContratacionView, self).form_valid(form)