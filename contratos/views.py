from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin

from formadores.forms import LegalizacionForm as LegalizacionFormFormadores
from formadores.forms import LegalizacionSeguridadForm as LegalizacionSeguridadFormFormadores
from lideres.forms import LegalizacionForm as LegalizacionFormLideres
from negociadores.forms import LegalizacionForm as LegalizacionFormNegociadores

from formadores.models import Contrato as ContratosFormadores
from lideres.models import Contrato as ContratosLideres
from negociadores.forms import Contrato as ContratosNegociadores

from formadores.models import TipoSoporte as TipoSoporteFormador
from lideres.models import TipoSoporte as TipoSoporteLider
from negociadores.models import TipoSoporte as TipoSoporteNegociador

from formadores.models import Soporte as SoporteFormador
from lideres.models import Soporte as SoporteLider
from negociadores.models import Soporte as SoporteNegociador

import datetime
from django.shortcuts import HttpResponseRedirect
# Create your views here.


#------------------------------------------------1. LEGALIZACION--------------------------------------------------------

class LegalizacionContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/legalizacion/seleccion.html'
    permission_required = "permisos_sican.contratos.contratos_legalizar.ver"



class LegalizacionContratosAdministrativosView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/legalizacion/administrativos/lista.html'
    login_url = '../'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_administrativos.ver"),
        "any": ()
    }



#---------------------------------------------- 1.1 LEGALIZACION FORMADORES --------------------------------------------

class LegalizacionContratosFormadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/legalizacion/formadores/lista.html'
    login_url = '../'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_formadores.ver"),
        "any": ()
    }

class LegalizacionContratoFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              FormView):
    form_class = LegalizacionFormFormadores
    success_url = '../../'
    template_name = 'contratos/legalizacion/formadores/legalizacion.html'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_formadores.ver",
                "permisos_sican.contratos.contratos_formadores.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = ContratosFormadores.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(LegalizacionContratoFormadorView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            contrato = ContratosFormadores.objects.get(id = kwargs['id_contrato'])
        except:
            return HttpResponseRedirect('../../')

        else:
            if request.user == contrato.formador.usuario:
                return super(LegalizacionContratoFormadorView,self).dispatch(request,*args,**kwargs)
            else:
                return HttpResponseRedirect('../../')

    def get_initial(self):
        return {'id_contrato': self.kwargs['id_contrato']}

    def form_valid(self, form):
        contrato = ContratosFormadores.objects.get(id = self.kwargs['id_contrato'])
        for field in form.cleaned_data.keys():
            if field != 'ids':
                tipo = TipoSoporteFormador.objects.get(id = field)
                soporte, created = SoporteFormador.objects.get_or_create(contrato = contrato,formador = contrato.formador,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(LegalizacionContratoFormadorView,self).form_valid(form)

#------------------------------------------------ 1.2 LEGALIZACION LIDERES ---------------------------------------------

class LegalizacionContratosLideresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/legalizacion/lideres/lista.html'
    login_url = '../'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_lideres.ver"),
        "any": ()
    }

class LegalizacionContratoLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              FormView):
    form_class = LegalizacionFormLideres
    success_url = '../../'
    template_name = 'contratos/legalizacion/lideres/legalizacion.html'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_lideres.ver",
                "permisos_sican.contratos.contratos_lideres.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = ContratosLideres.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(LegalizacionContratoLiderView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            contrato = ContratosLideres.objects.get(id = kwargs['id_contrato'])
        except:
            return HttpResponseRedirect('../../')

        else:
            if request.user == contrato.lider.usuario:
                return super(LegalizacionContratoLiderView,self).dispatch(request,*args,**kwargs)
            else:
                return HttpResponseRedirect('../../')

    def get_initial(self):
        return {'id_contrato': self.kwargs['id_contrato']}

    def form_valid(self, form):
        contrato = ContratosLideres.objects.get(id = self.kwargs['id_contrato'])
        for field in form.cleaned_data.keys():
            if field != 'ids':
                tipo = TipoSoporteLider.objects.get(id = field)
                soporte, created = SoporteLider.objects.get_or_create(contrato = contrato,lider = contrato.lider,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(LegalizacionContratoLiderView,self).form_valid(form)

#--------------------------------------------- 1.3 LEGALIZACION NEGOCIADORES -------------------------------------------

class LegalizacionContratosNegociadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/legalizacion/negociadores/lista.html'
    login_url = '../'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_negociadores.ver"),
        "any": ()
    }

class LegalizacionContratoNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              FormView):
    form_class = LegalizacionFormNegociadores
    success_url = '../../'
    template_name = 'contratos/legalizacion/negociadores/legalizacion.html'
    permissions = {
        "all": ("permisos_sican.contratos.contratos_legalizar.ver",
                "permisos_sican.contratos.contratos_negociadores.ver",
                "permisos_sican.contratos.contratos_negociadores.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = ContratosNegociadores.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(LegalizacionContratoNegociadorView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            contrato = ContratosNegociadores.objects.get(id = kwargs['id_contrato'])
        except:
            return HttpResponseRedirect('../../')

        else:
            if request.user == contrato.negociador.usuario:
                return super(LegalizacionContratoNegociadorView,self).dispatch(request,*args,**kwargs)
            else:
                return HttpResponseRedirect('../../')

    def get_initial(self):
        return {'id_contrato': self.kwargs['id_contrato']}

    def form_valid(self, form):
        contrato = ContratosNegociadores.objects.get(id = self.kwargs['id_contrato'])
        for field in form.cleaned_data.keys():
            if field != 'ids':
                tipo = TipoSoporteNegociador.objects.get(id = field)
                soporte, created = SoporteNegociador.objects.get_or_create(contrato = contrato,negociador = contrato.negociador,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(LegalizacionContratoNegociadorView,self).form_valid(form)

#-----------------------------------------------------------------------------------------------------------------------



#------------------------------------------------2. SEGURIDAD SOCIAL----------------------------------------------------

class SeguridadSocialView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    '''
    template_name = 'contratos/legalizacion/seguridad_social.html'
    permission_required = "permisos_sican.seguridad_social.ss_seguridad_social.ver"


class SeguridadSocialAdministrativosView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/seguridad_social/administrativos/lista.html'
    login_url = '../'
    permissions = {
        "all": ("permisos_sican.seguridad_social.ss_seguridad_social.ver",
                "permisos_sican.seguridad_social.ss_seguridad_social_administrativos.ver"),
        "any": ()
    }


#------------------------------------------- 2.1 SEGURIDAD SOCIAL LIDERES ----------------------------------------------

class SeguridadSocialFormadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'contratos/seguridad_social/formadores/lista.html'
    login_url = '../'
    permissions = {
        "all": ("permisos_sican.seguridad_social.ss_seguridad_social.ver",
                "permisos_sican.seguridad_social.ss_seguridad_social_formadores.ver"),
        "any": ()
    }

class SeguridadSocialFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              FormView):
    form_class = LegalizacionSeguridadFormFormadores
    success_url = '../../'
    template_name = 'contratos/seguridad_social/formadores/seguridad_social.html'
    permissions = {
        "all": ("permisos_sican.seguridad_social.ss_seguridad_social.ver",
                "permisos_sican.seguridad_social.ss_seguridad_social_formadores.ver",
                "permisos_sican.seguridad_social.ss_seguridad_social_formadores.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['nombre_contrato'] = ContratosFormadores.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(SeguridadSocialFormadorView,self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            contrato = ContratosFormadores.objects.get(id = kwargs['id_contrato'])
        except:
            return HttpResponseRedirect('../../')

        else:
            if request.user == contrato.formador.usuario:
                return super(SeguridadSocialFormadorView,self).dispatch(request,*args,**kwargs)
            else:
                return HttpResponseRedirect('../../')

    def get_initial(self):
        return {'id_contrato': self.kwargs['id_contrato']}

    def form_valid(self, form):
        contrato = ContratosFormadores.objects.get(id = self.kwargs['id_contrato'])
        for field in form.cleaned_data.keys():
            if field != 'ids':
                tipo = TipoSoporteFormador.objects.get(id = field)
                soporte, created = SoporteFormador.objects.get_or_create(contrato = contrato,formador = contrato.formador,tipo = tipo)
                soporte.fecha = datetime.datetime.now().date()
                soporte.archivo = form.cleaned_data[field]
                soporte.save()
        return super(SeguridadSocialFormadorView,self).form_valid(form)