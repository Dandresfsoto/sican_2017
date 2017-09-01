from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from lideres.forms import ConsultaLider
from lideres.models import Lideres
from lideres.models import Soporte
from lideres.forms import LegalizacionLideresForm
from rh.models import TipoSoporte
from django.shortcuts import HttpResponseRedirect
import datetime
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from lideres.forms import LegalizacionSeguridadForm, LegalizacionForm
from lideres.models import Contrato




#----------------------------------- LEGALIZACION DE CONTRATO ----------------------------------------------------------

class LegalizacionContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de lideres y cantidad de contratos de cada uno
    '''
    template_name = 'lideres/legalizacion/general/lista.html'
    permission_required = "permisos_sican.lideres.legalizacion.ver"



class LegalizacionContratoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):
    form_class = LegalizacionForm
    success_url = '../../'
    template_name = 'lideres/legalizacion/general/general.html'
    permission_required = "permisos_sican.lideres.legalizacion.general"

    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = Contrato.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(LegalizacionContratoView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == Contrato.objects.get(id = kwargs['id_contrato']).lider.usuario:
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
                soporte, created = Soporte.objects.get_or_create(contrato = contrato,lider = contrato.lider,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(LegalizacionContratoView,self).form_valid(form)



class LegalizacionSeguridadView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de lideres y cantidad de contratos de cada uno
    '''
    template_name = 'lideres/legalizacion/seguridadsocial/lista.html'
    permission_required = "permisos_sican.lideres.seguridadsocial.ver"


class SoportesSeguridadSocialView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              FormView):
    form_class = LegalizacionSeguridadForm
    success_url = '../../'
    template_name = 'lideres/legalizacion/seguridadsocial/seguridadsocial.html'
    permission_required = "permisos_sican.lideres.legalizacion.general"

    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = Contrato.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(SoportesSeguridadSocialView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user == Contrato.objects.get(id = kwargs['id_contrato']).lider.usuario:
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
                soporte, created = Soporte.objects.get_or_create(contrato = contrato,lider = contrato.lider,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(SoportesSeguridadSocialView,self).form_valid(form)

#-----------------------------------------------------------------------------------------------------------------------





# Create your views here.
class InicioView(FormView):
    form_class = ConsultaLider
    template_name = 'lideres/inicio.html'

    def form_valid(self, form):
        cedula = form.cleaned_data['cedula']
        return HttpResponseRedirect('/lideres/'+str(cedula))


class VinculosView(TemplateView):
    template_name = 'lideres/vinculos/vinculos.html'

    def get_context_data(self, **kwargs):
        lider = Lideres.objects.get(cedula=kwargs['cedula'])

        try:
            contrato = Soporte.objects.filter(lider=lider,oculto=False).get(tipo__id=10)
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['lider'] = lider.get_full_name()
        kwargs['tipo'] = lider.cargo.nombre
        kwargs['link_contrato'] = link
        kwargs['cargo'] = lider.cargo.nombre

        return super(VinculosView,self).get_context_data(**kwargs)


class LegalizacionView(UpdateView):
    template_name = "lideres/legalizacion.html"
    success_url = "completo/"
    form_class = LegalizacionLideresForm
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
                Soporte.objects.filter(lider=self.object, oculto=False).get(tipo__id=value)
            except:
                nuevo = Soporte(lider=self.object,fecha=datetime.datetime.now(),tipo=TipoSoporte.objects.get(id=value))
                nuevo.save()
            else:
                pass
        return self.render_to_response(self.get_context_data())



    def get_object(self, queryset=None):
        return Lideres.objects.get(cedula=self.kwargs['cedula'])


    def form_valid(self, form):
        soportes = Soporte.objects.filter(lider=self.object,oculto=False)
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
    template_name = 'lideres/legalizacion_completa.html'

    def get_context_data(self, **kwargs):
        lider = Lideres.objects.get(cedula=kwargs['cedula'])
        try:
            contrato = Soporte.objects.filter(lider=lider).get(nombre="Contrato")
        except:
            link = '#'
        else:
            link = contrato.get_archivo_url()

        kwargs['lider'] = lider.nombres + " " + lider.apellidos
        kwargs['tipo'] = lider.cargo.nombre
        kwargs['link_contrato'] = link
        return super(LegalizacionCompletaView,self).get_context_data(**kwargs)