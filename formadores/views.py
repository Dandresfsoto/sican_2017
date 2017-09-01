from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from formadores.forms import ConsultaFormador, LegalizacionForm
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import HttpResponseRedirect
from formadores.models import TipoSoporte
from formadores.models import Formador, Soporte
from django.shortcuts import HttpResponseRedirect
from formadores.tables import SolicitudTable, EntregablesTable, CortesTable, RevisionTable, PagoTable, TipologiasTable
from formadores.models import SolicitudTransporte, Desplazamiento
from formadores.forms import NuevaSolicitudTransportes, SubirSoporteForm, SeguridadSocialForm
from departamentos.models import Departamento
from municipios.models import Municipio
import datetime
from formadores.forms import OtroSiForm
from productos.models import Entregable
from formadores.models import Cortes, Revision
from django.utils import timezone
from cargos.models import Cargo
from formadores.models import Contrato
from formadores.forms import LegalizacionSeguridadForm

#----------------------------------- LEGALIZACION DE CONTRATO ----------------------------------------------------------

class LegalizacionContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'formadores/legalizacion/general/lista.html'
    permission_required = "permisos_sican.formadores.legalizacion.ver"



class LegalizacionContratoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):
    form_class = LegalizacionForm
    success_url = '../../'
    template_name = 'formadores/legalizacion/general/general.html'
    permission_required = "permisos_sican.formadores.legalizacion.general"

    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = Contrato.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(LegalizacionContratoView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == Contrato.objects.get(id = kwargs['id_contrato']).formador.usuario:
            return super(LegalizacionContratoView,self).dispatch(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('../../')

    def get_initial(self):
        return {'id_contrato': self.kwargs['id_contrato']}

    def form_valid(self, form):
        contrato = Contrato.objects.get(id = self.kwargs['id_contrato'])
        for field in form.cleaned_data.keys():
            if field != 'ids':
                tipo = TipoSoporte.objects.get(id = field)
                soporte, created = Soporte.objects.get_or_create(contrato = contrato,formador = contrato.formador,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(LegalizacionContratoView,self).form_valid(form)



class LegalizacionSeguridadView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'formadores/legalizacion/seguridadsocial/lista.html'
    permission_required = "permisos_sican.formadores.seguridadsocial.ver"


class SoportesSeguridadSocialView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):
    form_class = LegalizacionSeguridadForm
    success_url = '../../'
    template_name = 'formadores/legalizacion/seguridadsocial/seguridadsocial.html'
    permission_required = "permisos_sican.formadores.legalizacion.general"

    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = Contrato.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(SoportesSeguridadSocialView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == Contrato.objects.get(id = kwargs['id_contrato']).formador.usuario:
            return super(SoportesSeguridadSocialView,self).dispatch(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('../../')

    def get_initial(self):
        return {'id_contrato': self.kwargs['id_contrato']}

    def form_valid(self, form):
        contrato = Contrato.objects.get(id = self.kwargs['id_contrato'])
        for field in form.cleaned_data.keys():
            if field != 'ids':
                tipo = TipoSoporte.objects.get(id = field)
                soporte, created = Soporte.objects.get_or_create(contrato = contrato,formador = contrato.formador,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(SoportesSeguridadSocialView,self).form_valid(form)

#-----------------------------------------------------------------------------------------------------------------------


class InicioView(FormView):
    form_class = ConsultaFormador
    template_name = 'formadores/inicio.html'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        return HttpResponseRedirect('/formadores/'+str(cedula))


class VinculosView(TemplateView):
    template_name = 'formadores/vinculos/vinculos.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])

        try:
            contrato = Soporte.objects.filter(formador=formador,oculto=False).get(tipo__id=10)
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        kwargs['link_contrato'] = link

        dic = {
            '1':{
                'Formador Tipo 1':'Diplomados R1.pdf',
                'Formador Tipo 2':'Diplomados R1.pdf',
                'Formador Tipo 3':'Diplomados R1.pdf',
                'Formador Tipo 4':'Escuela Tic R1.pdf',
            },
            '2':{
                'Formador Tipo 1':'Diplomados R2.pdf',
                'Formador Tipo 2':'Diplomados R2.pdf',
                'Formador Tipo 3':'Diplomados R2.pdf',
                'Formador Tipo 4':'Escuela Tic R2.pdf',
            },
        }

        kwargs['carta'] = '/static/documentos/'+dic[str(formador.region.all()[0].numero)][formador.cargo.all()[0].nombre]
        kwargs['cargo'] = formador.get_cargo_string()

        return super(VinculosView,self).get_context_data(**kwargs)

class LegalizacionView(UpdateView):
    template_name = "formadores/legalizacion.html"
    success_url = "completo/"
    form_class = LegalizacionForm
    dic = {
            'rut':6,
            'cedula':2,
            'policia':4,
            'procuraduria':5,
            'contraloria':11,
            'certificacion':9,
            'seguridad_social':8
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        for key, value in self.dic.iteritems():
            try:
                Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=value)
            except:
                nuevo = Soporte(formador=self.object,fecha=datetime.datetime.now(),tipo=TipoSoporte.objects.get(id=value))
                nuevo.save()
            else:
                pass
        return self.render_to_response(self.get_context_data())



    def get_object(self, queryset=None):
        return Formador.objects.get(cedula=self.kwargs['cedula'])


    def form_valid(self, form):
        soportes = Soporte.objects.filter(formador=self.object,oculto=False)
        self.object.celular_personal = form.cleaned_data['celular_personal']
        self.object.correo_personal = form.cleaned_data['correo_personal']
        self.object.numero_cuenta = form.cleaned_data['numero_cuenta']
        self.object.profesion = form.cleaned_data['profesion']
        self.object.tipo_cuenta = form.cleaned_data['tipo_cuenta']
        self.object.banco = form.cleaned_data['banco']
        self.object.save()

        rut = soportes.get(tipo__id=self.dic['rut'])
        rut.archivo = form.cleaned_data['rut']
        rut.save()


        cedula = soportes.get(tipo__id=self.dic['cedula'])
        cedula.archivo = form.cleaned_data['fotocopia_cedula']
        cedula.save()

        policia = soportes.get(tipo__id=self.dic['policia'])
        policia.archivo = form.cleaned_data['antecedentes_judiciales']
        policia.save()

        procuraduria = soportes.get(tipo__id=self.dic['procuraduria'])
        procuraduria.archivo = form.cleaned_data['antecedentes_procuraduria']
        procuraduria.save()

        contraloria = soportes.get(tipo__id=self.dic['contraloria'])
        contraloria.archivo = form.cleaned_data['antecedentes_contraloria']
        contraloria.save()

        certificacion = soportes.get(tipo__id=self.dic['certificacion'])
        certificacion.archivo = form.cleaned_data['certificacion']
        certificacion.save()

        seguridad_social = soportes.get(tipo__id=self.dic['seguridad_social'])
        seguridad_social.archivo = form.cleaned_data['seguridad_social']
        seguridad_social.save()


        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        return {'cedula':self.object.cedula}

class LegalizacionCompletaView(TemplateView):
    template_name = 'formadores/legalizacion_completa.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])
        try:
            contrato = Soporte.objects.filter(formador=formador).get(nombre="Contrato")
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        kwargs['link_contrato'] = link
        return super(LegalizacionCompletaView,self).get_context_data(**kwargs)

class TransportesView(TemplateView):
    template_name = 'formadores/transportes/tabla.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])
        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        query = SolicitudTransporte.objects.filter(formador=formador)
        kwargs['table'] = SolicitudTable(query)
        return super(TransportesView,self).get_context_data(**kwargs)

class NuevaSolicitudTransportesView(FormView):
    template_name = "formadores/transportes/nuevo.html"
    form_class = NuevaSolicitudTransportes
    success_url = '../'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        return super(NuevaSolicitudTransportesView,self).get_context_data(**kwargs)

    def form_valid(self, form):



        desplazamientos = [
            {
                'fecha':form.cleaned_data['fecha_1'],
                'd_origen':form.cleaned_data['departamento_origen_1'],
                'm_origen':form.cleaned_data['municipio_origen_1'],
                'd_destino':form.cleaned_data['departamento_destino_1'],
                'm_destino':form.cleaned_data['municipio_destino_1'],
                'valor':float(form.cleaned_data['valor_1'].replace(',','')) if form.cleaned_data['valor_1'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_1']
            },
            {
                'fecha':form.cleaned_data['fecha_2'],
                'd_origen':form.cleaned_data['departamento_origen_2'],
                'm_origen':form.cleaned_data['municipio_origen_2'],
                'd_destino':form.cleaned_data['departamento_destino_2'],
                'm_destino':form.cleaned_data['municipio_destino_2'],
                'valor':float(form.cleaned_data['valor_2'].replace(',','')) if form.cleaned_data['valor_2'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_2']
            },
            {
                'fecha':form.cleaned_data['fecha_3'],
                'd_origen':form.cleaned_data['departamento_origen_3'],
                'm_origen':form.cleaned_data['municipio_origen_3'],
                'd_destino':form.cleaned_data['departamento_destino_3'],
                'm_destino':form.cleaned_data['municipio_destino_3'],
                'valor':float(form.cleaned_data['valor_3'].replace(',','')) if form.cleaned_data['valor_3'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_3']
            },
            {
                'fecha':form.cleaned_data['fecha_4'],
                'd_origen':form.cleaned_data['departamento_origen_4'],
                'm_origen':form.cleaned_data['municipio_origen_4'],
                'd_destino':form.cleaned_data['departamento_destino_4'],
                'm_destino':form.cleaned_data['municipio_destino_4'],
                'valor':float(form.cleaned_data['valor_4'].replace(',','')) if form.cleaned_data['valor_4'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_4']
            },
            {
                'fecha':form.cleaned_data['fecha_5'],
                'd_origen':form.cleaned_data['departamento_origen_5'],
                'm_origen':form.cleaned_data['municipio_origen_5'],
                'd_destino':form.cleaned_data['departamento_destino_5'],
                'm_destino':form.cleaned_data['municipio_destino_5'],
                'valor':float(form.cleaned_data['valor_5'].replace(',','')) if form.cleaned_data['valor_5'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_5']
            },
            {
                'fecha':form.cleaned_data['fecha_6'],
                'd_origen':form.cleaned_data['departamento_origen_6'],
                'm_origen':form.cleaned_data['municipio_origen_6'],
                'd_destino':form.cleaned_data['departamento_destino_6'],
                'm_destino':form.cleaned_data['municipio_destino_6'],
                'valor':float(form.cleaned_data['valor_6'].replace(',','')) if form.cleaned_data['valor_6'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_6']
            },
            {
                'fecha':form.cleaned_data['fecha_7'],
                'd_origen':form.cleaned_data['departamento_origen_7'],
                'm_origen':form.cleaned_data['municipio_origen_7'],
                'd_destino':form.cleaned_data['departamento_destino_7'],
                'm_destino':form.cleaned_data['municipio_destino_7'],
                'valor':float(form.cleaned_data['valor_7'].replace(',','')) if form.cleaned_data['valor_7'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_7']
            },
            {
                'fecha':form.cleaned_data['fecha_8'],
                'd_origen':form.cleaned_data['departamento_origen_8'],
                'm_origen':form.cleaned_data['municipio_origen_8'],
                'd_destino':form.cleaned_data['departamento_destino_8'],
                'm_destino':form.cleaned_data['municipio_destino_8'],
                'valor':float(form.cleaned_data['valor_8'].replace(',','')) if form.cleaned_data['valor_8'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_8']
            },
            {
                'fecha':form.cleaned_data['fecha_9'],
                'd_origen':form.cleaned_data['departamento_origen_9'],
                'm_origen':form.cleaned_data['municipio_origen_9'],
                'd_destino':form.cleaned_data['departamento_destino_9'],
                'm_destino':form.cleaned_data['municipio_destino_9'],
                'valor':float(form.cleaned_data['valor_9'].replace(',','')) if form.cleaned_data['valor_9'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_9']
            },
            {
                'fecha':form.cleaned_data['fecha_10'],
                'd_origen':form.cleaned_data['departamento_origen_10'],
                'm_origen':form.cleaned_data['municipio_origen_10'],
                'd_destino':form.cleaned_data['departamento_destino_10'],
                'm_destino':form.cleaned_data['municipio_destino_10'],
                'valor':float(form.cleaned_data['valor_10'].replace(',','')) if form.cleaned_data['valor_10'] != u'' else 0,
                'motivo':form.cleaned_data['motivo_10']
            },
        ]

        desplazamientos_obj = []

        valor = 0

        for desplazamiento in desplazamientos:
            if desplazamiento['valor'] != None:
                if desplazamiento['fecha'] != '':
                    if desplazamiento['d_origen'] != '':
                        if desplazamiento['m_origen'] != '':
                            if desplazamiento['d_destino'] != '':
                                if desplazamiento['m_destino'] != '':
                                    if desplazamiento['motivo'] != '':
                                        valor += desplazamiento['valor']
                                        desplazamientos_obj.append(Desplazamiento.objects.create(
                                            departamento_origen=Departamento.objects.get(id=desplazamiento['d_origen']),
                                            municipio_origen=Municipio.objects.get(id=desplazamiento['m_origen']),
                                            departamento_destino=Departamento.objects.get(id=desplazamiento['d_destino']),
                                            municipio_destino=Municipio.objects.get(id=desplazamiento['m_destino']),
                                            valor=desplazamiento['valor'],
                                            fecha = desplazamiento['fecha'],
                                            motivo = desplazamiento['motivo']
                                        ))

        solicitud = SolicitudTransporte.objects.create(
            creacion_date = timezone.now(),
            formador = Formador.objects.get(cedula=self.kwargs['cedula']),
            nombre = form.cleaned_data['nombre'],
            valor = valor
        )

        for desplazamiento_obj in desplazamientos_obj:
            solicitud.desplazamientos.add(desplazamiento_obj)

        solicitud.save()



        return super(NuevaSolicitudTransportesView,self).form_valid(form)

class SubirSoporteTransportesView(UpdateView):
    template_name = "formadores/transportes/subir_soporte.html"
    model = SolicitudTransporte
    success_url = "../../"
    pk_url_kwarg = 'id_soporte'
    form_class = SubirSoporteForm

class OtroSiView(UpdateView):
    template_name = "formadores/otrosi/formulario.html"
    success_url = "completo/"
    form_class = OtroSiForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())



    def get_object(self, queryset=None):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        soporte = Soporte.objects.filter(formador = formador,tipo = TipoSoporte.objects.get(nombre="Otro si - Firmado"))
        if soporte.count() == 1:
            soporte = soporte[0]
        else:
            soporte = Soporte.objects.create(formador = formador,fecha = datetime.datetime.now().date(),tipo = TipoSoporte.objects.get(nombre="Otro si - Firmado"))

        return soporte

    def get_context_data(self, **kwargs):
        url = Soporte.objects.filter(formador__cedula=self.kwargs['cedula']).get(tipo__nombre="Otro si - Blanco").get_archivo_url()
        kwargs['otro_si_blanco'] = url
        return super(OtroSiView,self).get_context_data(**kwargs)

class OtroSiCompletoView(TemplateView):
    template_name = 'formadores/otrosi/completo.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])
        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        return super(OtroSiCompletoView,self).get_context_data(**kwargs)

class EntregablesView(TemplateView):
    template_name = 'formadores/entregables/entregables.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.get_full_name()
        kwargs['tipo'] = formador.get_cargo_string()

        nombre = Cargo.objects.get(id = self.kwargs['id_cargo']).nombre

        if nombre == "Formador Tipo 1":
            numero_diplomado = 1
        elif nombre == "Formador Tipo 2":
            numero_diplomado = 2
        elif nombre == "Formador Tipo 3":
            numero_diplomado = 3
        elif nombre == "Formador Tipo 4":
            numero_diplomado = 4
        else:
            numero_diplomado = 0

        query = Entregable.objects.all().filter(sesion__nivel__diplomado__numero = numero_diplomado).order_by('numero')
        kwargs['table'] = EntregablesTable(query)
        return super(EntregablesView,self).get_context_data(**kwargs)



class TipologiasView(TemplateView):
    template_name = 'formadores/entregables/tipologias.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.get_full_name()
        kwargs['tipo'] = formador.get_cargo_string()

        query = formador.cargo.all()
        kwargs['table'] = TipologiasTable(query)
        return super(TipologiasView,self).get_context_data(**kwargs)



class PagosView(TemplateView):
    template_name = 'formadores/pagos/cortes.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.get_full_name()
        kwargs['tipo'] = formador.get_cargo_string()

        nombre = Cargo.objects.get(id = self.kwargs['id_cargo'])

        if nombre == "Formador Tipo 1":
            numero_diplomado = 1
        elif nombre == "Formador Tipo 2":
            numero_diplomado = 2
        elif nombre == "Formador Tipo 3":
            numero_diplomado = 3
        elif nombre == "Formador Tipo 4":
            numero_diplomado = 4
        else:
            numero_diplomado = 0

        revisiones = []

        for revision in Revision.objects.filter(formador_revision = formador):
            
            valor = 0
            for producto in revision.productos.all():
                valor += producto.cantidad * producto.valor_entregable.valor
            if valor > 0 and revision.corte != None:
                revisiones.append(revision.corte.id)

        kwargs['table'] = CortesTable(Cortes.objects.filter(id__in = revisiones),id_formador = formador.id)
        return super(PagosView,self).get_context_data(**kwargs)



class TipologiasPagosView(TemplateView):
    template_name = 'formadores/pagos/tipologias.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.get_full_name()
        kwargs['tipo'] = formador.get_cargo_string()


        query = formador.cargo.all()
        kwargs['table'] = TipologiasTable(query)
        return super(TipologiasPagosView,self).get_context_data(**kwargs)


class PagosCorteView(TemplateView):
    template_name = 'formadores/pagos/pagos_corte.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.get_full_name()
        kwargs['tipo'] = formador.get_cargo_string()

        nombre = Cargo.objects.get(id = self.kwargs['id_cargo'])

        if nombre == "Formador Tipo 1":
            numero_diplomado = 1
        elif nombre == "Formador Tipo 2":
            numero_diplomado = 2
        elif nombre == "Formador Tipo 3":
            numero_diplomado = 3
        elif nombre == "Formador Tipo 4":
            numero_diplomado = 4
        else:
            numero_diplomado = 0

        corte = Cortes.objects.get(id = self.kwargs['id_corte'])
        revisiones = []

        for revision in Revision.objects.filter(formador_revision = formador,corte = corte):
            valor = 0
            for producto in revision.productos.all():
                valor += producto.cantidad * producto.valor_entregable.valor
            if valor > 0:
                revisiones.append(revision.id)

        kwargs['table'] = RevisionTable(Revision.objects.filter(id__in = revisiones))
        return super(PagosCorteView,self).get_context_data(**kwargs)

class PagosCorteEntregableView(TemplateView):
    template_name = 'formadores/pagos/pagos_corte.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.get_full_name()
        kwargs['tipo'] = formador.get_cargo_string()

        nombre = Cargo.objects.get(id = self.kwargs['id_cargo'])

        if nombre == "Formador Tipo 1":
            numero_diplomado = 1
        elif nombre == "Formador Tipo 2":
            numero_diplomado = 2
        elif nombre == "Formador Tipo 3":
            numero_diplomado = 3
        elif nombre == "Formador Tipo 4":
            numero_diplomado = 4
        else:
            numero_diplomado = 0

        revision = Revision.objects.get(id = self.kwargs['id_pago'])
        kwargs['table'] = PagoTable(revision.productos.exclude(cantidad = 0))
        return super(PagosCorteEntregableView,self).get_context_data(**kwargs)

class SeguridadSocialView(FormView):
    template_name = "formadores/seguridadsocial/seguridadform.html"
    form_class = SeguridadSocialForm
    success_url = 'completo'
    dic = {
            'agosto':8,
            'septiembre':17,
            'octubre':18,
            'noviembre':19,
            'diciembre':20
    }

    def get_object(self, queryset=None):
        return Formador.objects.get(cedula=self.kwargs['cedula'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        for key, value in self.dic.iteritems():
            try:
                Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=value)
            except:
                nuevo = Soporte(formador=self.object,fecha=datetime.datetime.now(),tipo=TipoSoporte.objects.get(id=value))
                nuevo.save()
            else:
                pass
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=self.kwargs['cedula'])
        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        kwargs['cedula'] = formador.cedula
        return super(SeguridadSocialView,self).get_context_data(**kwargs)

    def get_initial(self):
        return {'cedula':self.kwargs['cedula']}

    def form_valid(self, form):
        self.object = self.get_object()
        agosto_db = Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=self.dic['agosto'])
        septiembre_db = Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=self.dic['septiembre'])
        octubre_db = Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=self.dic['octubre'])
        noviembre_db = Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=self.dic['noviembre'])
        diciembre_db = Soporte.objects.filter(formador=self.object, oculto=False).get(tipo__id=self.dic['diciembre'])

        agosto = form.cleaned_data['agosto']
        septiembre = form.cleaned_data['septiembre']
        octubre = form.cleaned_data['octubre']
        noviembre = form.cleaned_data['noviembre']
        diciembre = form.cleaned_data['diciembre']

        if agosto != False:
            agosto_db.archivo = agosto
        else:
            agosto_db.archivo = None


        if septiembre != False:
            septiembre_db.archivo = septiembre
        else:
            septiembre_db.archivo = None


        if octubre != False:
            octubre_db.archivo = octubre
        else:
            octubre_db.archivo = None


        if noviembre != False:
            noviembre_db.archivo = noviembre
        else:
            noviembre_db.archivo = None


        if diciembre != False:
            diciembre_db.archivo = diciembre
        else:
            diciembre_db.archivo = None

        agosto_db.save()
        septiembre_db.save()
        octubre_db.save()
        noviembre_db.save()
        diciembre_db.save()


        return super(SeguridadSocialView,self).form_valid(form)

class SeguridadSocialCompletaView(TemplateView):
    template_name = 'formadores/seguridadsocial/completo.html'

    def get_context_data(self, **kwargs):
        formador = Formador.objects.get(cedula=kwargs['cedula'])
        try:
            contrato = Soporte.objects.filter(formador=formador).get(nombre="Contrato")
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['formador'] = formador.nombres + " " + formador.apellidos
        kwargs['tipo'] = formador.get_cargo_string()
        kwargs['link_contrato'] = link
        return super(SeguridadSocialCompletaView,self).get_context_data(**kwargs)