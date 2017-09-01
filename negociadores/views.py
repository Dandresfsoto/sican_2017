from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from lideres.models import Soporte
from rh.models import TipoSoporte
from django.shortcuts import HttpResponseRedirect
import datetime
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from negociadores.forms import LegalizacionSeguridadForm, LegalizacionForm
from negociadores.models import Contrato




#----------------------------------- LEGALIZACION DE CONTRATO ----------------------------------------------------------

class LegalizacionContratosView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de negociadores y cantidad de contratos de cada uno
    '''
    template_name = 'negociadores/legalizacion/general/lista.html'
    permission_required = "permisos_sican.negociadores.legalizacion.ver"



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