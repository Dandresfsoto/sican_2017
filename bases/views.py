from administrativos.models import Administrativo, Soporte
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from administrativos.forms import NuevoForm, NuevoSoporteForm
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from departamentos.models import Departamento
from departamentos.forms import DepartamentoForm
from municipios.models import Municipio
from municipios.forms import MunicipioForm
from secretarias.models import Secretaria
from secretarias.forms import SecretariaForm
from radicados.models import Radicado
from radicados.forms import RadicadoForm
from django.http import HttpResponseRedirect

class DepartamentoListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'bases/departamentos/lista.html'
    permission_required = "permisos_sican.bases.departamentos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.bases.departamentos.crear')
        return super(DepartamentoListView, self).get_context_data(**kwargs)

class NuevoDepartamentoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Departamento
    form_class = DepartamentoForm
    success_url = '/bases/departamentos/'
    template_name = 'bases/departamentos/nuevo.html'
    permission_required = "permisos_sican.bases.departamentos.crear"

class UpdateDepartamentoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    pk_url_kwarg = 'pk'
    success_url = '/bases/departamentos/'
    template_name = 'bases/departamentos/editar.html'
    permission_required = "permisos_sican.bases.departamentos.editar"

class DeleteDepartamentoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Departamento
    pk_url_kwarg = 'pk'
    success_url = '/bases/departamentos/'
    template_name = 'bases/departamentos/eliminar.html'
    permission_required = "permisos_sican.bases.departamentos.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class MunicipioListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'bases/municipios/lista.html'
    permission_required = "permisos_sican.bases.municipios.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.bases.municipios.crear')
        return super(MunicipioListView, self).get_context_data(**kwargs)

class NuevoMunicipioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Municipio
    form_class = MunicipioForm
    success_url = '/bases/municipios/'
    template_name = 'bases/municipios/nuevo.html'
    permission_required = "permisos_sican.bases.municipios.crear"

class UpdateMunicipioView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Municipio
    form_class = MunicipioForm
    pk_url_kwarg = 'pk'
    success_url = '/bases/municipios/'
    template_name = 'bases/municipios/editar.html'
    permission_required = "permisos_sican.bases.municipios.editar"

class DeleteMunicipioView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Municipio
    pk_url_kwarg = 'pk'
    success_url = '/bases/municipios/'
    template_name = 'bases/municipios/eliminar.html'
    permission_required = "permisos_sican.bases.municipios.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class SecretariaListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'bases/secretarias/lista.html'
    permission_required = "permisos_sican.bases.secretarias.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.bases.secretarias.crear')
        return super(SecretariaListView, self).get_context_data(**kwargs)

class NuevoSecretariaView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Secretaria
    form_class = SecretariaForm
    success_url = '/bases/secretarias/'
    template_name = 'bases/secretarias/nuevo.html'
    permission_required = "permisos_sican.bases.secretarias.crear"

class UpdateSecretariaView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Secretaria
    form_class = SecretariaForm
    pk_url_kwarg = 'pk'
    success_url = '/bases/secretarias/'
    template_name = 'bases/secretarias/editar.html'
    permission_required = "permisos_sican.bases.secretarias.editar"

class DeleteSecretariaView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Secretaria
    pk_url_kwarg = 'pk'
    success_url = '/bases/secretarias/'
    template_name = 'bases/secretarias/eliminar.html'
    permission_required = "permisos_sican.bases.secretarias.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)



class RadicadoListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'bases/radicados/lista.html'
    permission_required = "permisos_sican.bases.radicados.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.bases.radicados.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.bases.radicados.informes')
        return super(RadicadoListView, self).get_context_data(**kwargs)

class NuevoRadicadoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Radicado
    form_class = RadicadoForm
    success_url = '/bases/radicados/'
    template_name = 'bases/radicados/nuevo.html'
    permission_required = "permisos_sican.bases.radicados.crear"

class UpdateRadicadoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Radicado
    form_class = RadicadoForm
    pk_url_kwarg = 'pk'
    success_url = '/bases/radicados/'
    template_name = 'bases/radicados/editar.html'
    permission_required = "permisos_sican.bases.radicados.editar"

class DeleteRadicadoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Radicado
    pk_url_kwarg = 'pk'
    success_url = '/bases/radicados/'
    template_name = 'bases/radicados/eliminar.html'
    permission_required = "permisos_sican.bases.radicados.eliminar"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)