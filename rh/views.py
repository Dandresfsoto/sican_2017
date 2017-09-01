from administrativos.models import Administrativo, Soporte
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from administrativos.forms import NuevoForm, NuevoSoporteForm
from cargos.models import Cargo
from cargos.forms import NuevoCargoForm, EditarCargoForm
from django.http import HttpResponseRedirect
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from administrativos.forms import UpdateSoporteAdministrativoForm
from rh.models import TipoSoporte
from rh.forms import NuevoTipoSoporteForm
from formadores.models import Formador
from formadores.forms import FormadorForm, NuevoSoporteFormadorForm
from formadores.models import Soporte as SoporteFormador
from lideres.models import Soporte as SoporteLider
from negociadores.models import Soporte as SoporteNegociador
from lideres.models import Lideres
from lideres.forms import LideresForm, NuevoSoporteLiderForm
from negociadores.models import Negociador
from negociadores.forms import NegociadorForm, NuevoSoporteNegociadorForm
from rh.models import RequerimientoPersonal
from rh.forms import RequerimientoPersonalRh,RequerimientoPersonalRhEspera, RequerimientoPersonalRhContratar,RequerimientoPersonalRhDeserta
import datetime
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL,RECURSO_HUMANO_EMAIL
from formadores.models import Contrato as ContratoFormador
from formadores.forms import ContratoForm as ContratoFormadorForm
from formadores.models import SolicitudSoportes as SolicitudSoportesFormador
from formadores.forms import SolicitudSoportesFormadorForm
from lideres.models import Contrato as ContratoLider
from lideres.forms import ContratoForm as ContratoLiderForm
from lideres.models import SolicitudSoportes as SolicitudSoportesLider
from lideres.forms import SolicitudSoportesLiderForm
from negociadores.models import Contrato as ContratoNegociador
from negociadores.forms import ContratoForm as ContratoNegociadorForm
from negociadores.models import SolicitudSoportes as SolicitudSoportesNegociador
from negociadores.forms import SolicitudSoportesNegociadorForm
from formadores.models import CohortesFormadores
from formadores.forms import CohortesFormadoresForm
from formadores.tasks import cohorte_formadores

#------------------------------------------------ 1. PERSONAL ----------------------------------------------------------

class PersonalView(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   TemplateView):
    template_name = 'rh/personal/lista.html'
    permission_required = "permisos_sican.rh.rh_personal.ver"

    def get_context_data(self, **kwargs):
        kwargs['permiso_administrativo'] = self.request.user.has_perm('permisos_sican.rh.rh_administrativos.ver')
        kwargs['permiso_acceso'] = self.request.user.has_perm('permisos_sican.rh.rh_acceso.ver')
        kwargs['permiso_formadores'] = self.request.user.has_perm('permisos_sican.rh.rh_formadores.ver')
        kwargs['permiso_general'] = self.request.user.has_perm('permisos_sican.rh.rh_general.ver')
        return super(PersonalView,self).get_context_data(**kwargs)

#------------------------------------------ 1.1.1 ADMINISTRATIVOS ------------------------------------------------------

class AdministrativoView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/administrativos/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_administrativos.crear')
        return super(AdministrativoView, self).get_context_data(**kwargs)

class NuevoAdministrativoView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = Administrativo
    form_class = NuevoForm
    success_url = '../'
    template_name = 'rh/personal/administrativos/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos.crear"),
        "any": ()
    }


class UpdateAdministrativoView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = Administrativo
    form_class = NuevoForm
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/administrativos/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos.editar"),
        "any": ()
    }

class DeleteAdministrativoView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = Administrativo
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/administrativos/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos.eliminar"),
        "any": ()
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#--------------------------------------- 1.1.2 SOPORTES ADMINISTRATIVOS ------------------------------------------------

class SoporteAdministrativoView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/administrativos/soportes/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos_soportes.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_administrativo'] = kwargs['pk']
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_administrativos_soportes.crear')
        return super(SoporteAdministrativoView, self).get_context_data(**kwargs)


class NuevoSoporteAdministrativoView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = Soporte
    form_class = NuevoSoporteForm
    success_url = '../'
    template_name = 'rh/personal/administrativos/soportes/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos_soportes.ver",
                "permisos_sican.rh.rh_administrativos_soportes.crear"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=self.kwargs['pk']).get_full_name
        return super(NuevoSoporteAdministrativoView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'administrativo':self.kwargs['pk']}


class UpdateSoporteAdministrativoView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = Soporte
    form_class = UpdateSoporteAdministrativoForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/administrativos/soportes/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos_soportes.ver",
                "permisos_sican.rh.rh_administrativos_soportes.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteAdministrativoView, self).get_context_data(**kwargs)


class DeleteSoporteAdministrativoView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = Soporte
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/administrativos/soportes/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_administrativos.ver",
                "permisos_sican.rh.rh_administrativos_soportes.ver",
                "permisos_sican.rh.rh_administrativos_soportes.eliminar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_administrativo'] = Administrativo.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteAdministrativoView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#------------------------------------------------- 1.2 ACCESO ----------------------------------------------------------

class AccesoView(LoginRequiredMixin,
                   MultiplePermissionsRequiredMixin,
                   TemplateView):
    template_name = 'rh/personal/acceso/links.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['permiso_lideres'] = self.request.user.has_perm('permisos_sican.rh.rh_lideres.ver')
        kwargs['permiso_negociadores'] = self.request.user.has_perm('permisos_sican.rh.rh_negociadores.ver')
        return super(AccesoView,self).get_context_data(**kwargs)

#------------------------------------------- 1.2.1.1 ACCESO LIDERES ----------------------------------------------------

class LideresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/acceso/lideres/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_lideres.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_lideres.informes')
        return super(LideresView, self).get_context_data(**kwargs)

class NuevoLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = Lideres
    form_class = LideresForm
    success_url = '../'
    template_name = 'rh/personal/acceso/lideres/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres.crear"),
        "any": ()
    }

class UpdateLiderView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = Lideres
    form_class = LideresForm
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/acceso/lideres/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres.editar"),
        "any": ()
    }

class DeleteLiderView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = Lideres
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/acceso/lideres/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres.eliminar"),
        "any": ()
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#--------------------------------------- 1.2.1.2 ACCESO LIDERES SOPORTES -----------------------------------------------

class SoporteLiderView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/acceso/lideres/soportes/lista.html'
    permission_required = "permisos_sican.rh.lideres_soportes.ver"
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres_soportes.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_lider'] = kwargs['pk']
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_lideres_soportes.crear')
        return super(SoporteLiderView, self).get_context_data(**kwargs)

class NuevoSoporteLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = SoporteFormador
    form_class = NuevoSoporteLiderForm
    success_url = '../'
    template_name = 'rh/personal/acceso/lideres/soportes/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres_soportes.ver",
                "permisos_sican.rh.rh_lideres_soportes.crear"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name()
        return super(NuevoSoporteLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'lider':self.kwargs['pk']}

class UpdateSoporteLiderView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = SoporteLider
    form_class = NuevoSoporteLiderForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/lideres/soportes/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres_soportes.ver",
                "permisos_sican.rh.rh_lideres_soportes.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'lider':self.kwargs['pk']}

class DeleteSoporteLiderView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = SoporteLider
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/lideres/soportes/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_lideres.ver",
                "permisos_sican.rh.rh_lideres_soportes.ver",
                "permisos_sican.rh.rh_lideres_soportes.eliminar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_lider'] = Lideres.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteLiderView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#----------------------------------------- 1.2.2.1 ACCESO NEGOCIADORES -------------------------------------------------

class NegociadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/acceso/negociadores/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_negociadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_negociadores.informes')
        return super(NegociadoresView, self).get_context_data(**kwargs)


class NuevoNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = Negociador
    form_class = NegociadorForm
    success_url = '../'
    template_name = 'rh/personal/acceso/negociadores/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores.crear"),
        "any": ()
    }


class UpdateNegociadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = Negociador
    form_class = NegociadorForm
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/acceso/negociadores/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores.editar"),
        "any": ()
    }


class DeleteNegociadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = Negociador
    pk_url_kwarg = 'pk'
    success_url = '/rh/negociadores/'
    template_name = 'rh/personal/acceso/negociadores/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores.eliminar"),
        "any": ()
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#---------------------------------- 1.2.2.1 ACCESO NEGOCIADORES SOPORTES -----------------------------------------------

class SoporteNegociadorView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/acceso/negociadores/soportes/lista.html'
    permission_required = "permisos_sican.rh.rh_negociador_soportes.ver"
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores_soportes.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_negociador'] = Negociador.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_negociador'] = kwargs['pk']
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_negociadores_soportes.crear')
        return super(SoporteNegociadorView, self).get_context_data(**kwargs)

class NuevoSoporteNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = SoporteNegociador
    form_class = NuevoSoporteNegociadorForm
    success_url = '../'
    template_name = 'rh/personal/acceso/negociadores/soportes/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores_soportes.ver",
                "permisos_sican.rh.rh_negociadores_soportes.crear"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_negociador'] = Negociador.objects.get(id=self.kwargs['pk']).get_full_name()
        return super(NuevoSoporteNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'negociador':self.kwargs['pk']}

class UpdateSoporteNegociadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = SoporteNegociador
    form_class = NuevoSoporteNegociadorForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/negociadores/soportes/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores_soportes.ver",
                "permisos_sican.rh.rh_negociadores_soportes.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_negociador'] = Negociador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'negociador':self.kwargs['pk']}

class DeleteSoporteNegociadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = SoporteNegociador
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/acceso/negociadores/soportes/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_acceso.ver",
                "permisos_sican.rh.rh_negociadores.ver",
                "permisos_sican.rh.rh_negociadores_soportes.ver",
                "permisos_sican.rh.rh_negociadores_soportes.eliminar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_negociador'] = Negociador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteNegociadorView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#----------------------------------------------- 1.3 FORMACION ---------------------------------------------------------

class FormadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/formadores/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_formadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_formadores.informes')
        return super(FormadoresView, self).get_context_data(**kwargs)


class NuevoFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = Formador
    form_class = FormadorForm
    success_url = '../'
    template_name = 'rh/personal/formadores/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores.crear"),
        "any": ()
    }


class UpdateFormadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = Formador
    form_class = FormadorForm
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/formadores/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores.editar"),
        "any": ()
    }


class DeleteFormadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = Formador
    pk_url_kwarg = 'pk'
    success_url = '/rh/formadores/'
    template_name = 'rh/personal/formadores/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores.eliminar"),
        "any": ()
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#------------------------------------------ 1.3.1 FORMACION SOPORTES ---------------------------------------------------

class SoporteFormadorView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/personal/formadores/soportes/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores_soportes.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_formador'] = Formador.objects.get(id=kwargs['pk']).get_full_name
        kwargs['id_formador'] = kwargs['pk']
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_formadores_soportes.crear')
        return super(SoporteFormadorView, self).get_context_data(**kwargs)

class NuevoSoporteFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = SoporteFormador
    form_class = NuevoSoporteFormadorForm
    success_url = '../'
    template_name = 'rh/personal/formadores/soportes/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores_soportes.ver",
                "permisos_sican.rh.rh_formadores_soportes.crear"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_formador'] = Formador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(NuevoSoporteFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'formador':self.kwargs['pk']}

class UpdateSoporteFormadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               UpdateView):
    model = SoporteFormador
    form_class = NuevoSoporteFormadorForm
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/formadores/soportes/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores_soportes.ver",
                "permisos_sican.rh.rh_formadores_soportes.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['nombre_formador'] = Formador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(UpdateSoporteFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'formador':self.kwargs['pk']}

class DeleteSoporteFormadorView(LoginRequiredMixin,
                               MultiplePermissionsRequiredMixin,
                               DeleteView):
    model = SoporteFormador
    pk_url_kwarg = 'id_soporte'
    success_url = '../../'
    template_name = 'rh/personal/formadores/soportes/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_formadores.ver",
                "permisos_sican.rh.rh_formadores_soportes.ver",
                "permisos_sican.rh.rh_formadores_soportes.eliminar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre_formador'] = Formador.objects.get(id=self.kwargs['pk']).get_full_name
        return super(DeleteSoporteFormadorView, self).get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#-------------------------------------------------- 1.4 CARGOS ---------------------------------------------------------

class CargosView(LoginRequiredMixin,
                 MultiplePermissionsRequiredMixin,
                 TemplateView):
    template_name = 'rh/personal/cargos/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_cargos.ver"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_cargos.crear')
        return super(CargosView, self).get_context_data(**kwargs)

class NuevoCargoView(LoginRequiredMixin,
                     MultiplePermissionsRequiredMixin,
                     CreateView):
    model = Cargo
    form_class = NuevoCargoForm
    success_url = '../'
    template_name = 'rh/personal/cargos/nuevo.html'

    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_cargos.ver",
                "permisos_sican.rh.rh_cargos.crear"),
        "any": ()
    }

class UpdateCargoView(LoginRequiredMixin,
                      MultiplePermissionsRequiredMixin,
                      UpdateView):
    model = Cargo
    form_class = EditarCargoForm
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/cargos/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_cargos.ver",
                "permisos_sican.rh.rh_cargos.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        try:
            url = self.object.manual.url
        except:
            url = ""
        kwargs['manual_link'] = url
        kwargs['manual_filename'] = self.object.manual_filename
        return super(UpdateCargoView, self).get_context_data(**kwargs)

class DeleteCargoView(LoginRequiredMixin,
                      MultiplePermissionsRequiredMixin,
                      DeleteView):
    model = Cargo
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'rh/personal/cargos/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_cargos.ver",
                "permisos_sican.rh.rh_cargos.eliminar"),
        "any": ()
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#------------------------------------------------ 1.5 SOPORTES ---------------------------------------------------------

class TipoSoporteAdministrativoView(LoginRequiredMixin,
                 MultiplePermissionsRequiredMixin,
                 TemplateView):
    template_name = 'rh/personal/tipo_soporte/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_tipo_soporte.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_tipo_soporte.crear')
        return super(TipoSoporteAdministrativoView, self).get_context_data(**kwargs)

class NuevoTipoSoporteAdministrativoView(LoginRequiredMixin,
                     MultiplePermissionsRequiredMixin,
                     CreateView):
    model = TipoSoporte
    form_class = NuevoTipoSoporteForm
    success_url = '/rh/personal/tipo_soporte/'
    template_name = 'rh/personal/tipo_soporte/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_tipo_soporte.ver",
                "permisos_sican.rh.rh_tipo_soporte.crear"),
        "any": ()
    }

class UpdateTipoSoporteAdministrativoView(LoginRequiredMixin,
                      MultiplePermissionsRequiredMixin,
                      UpdateView):
    model = TipoSoporte
    form_class = NuevoTipoSoporteForm
    pk_url_kwarg = 'pk'
    success_url = '/rh/personal/tipo_soporte/'
    template_name = 'rh/personal/tipo_soporte/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_tipo_soporte.ver",
                "permisos_sican.rh.rh_tipo_soporte.editar"),
        "any": ()
    }

class DeleteTipoSoporteAdministrativoView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    model = TipoSoporte
    pk_url_kwarg = 'pk'
    success_url = '/rh/personal/tipo_soporte/'
    template_name = 'rh/personal/tipo_soporte/eliminar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_personal.ver",
                "permisos_sican.rh.rh_tipo_soporte.ver",
                "permisos_sican.rh.rh_tipo_soporte.eliminar"),
        "any": ()
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.oculto = True
        self.object.save()
        return HttpResponseRedirect(success_url)

#---------------------------------------------- 2. CONTRATACION --------------------------------------------------------

class ContratacionView(LoginRequiredMixin,
                   PermissionRequiredMixin,
                   TemplateView):
    template_name = 'rh/contratacion/lista.html'
    permission_required = "permisos_sican.rh.rh_contratacion.ver"

    def get_context_data(self, **kwargs):
        kwargs['permiso_formadores'] = self.request.user.has_perm('permisos_sican.rh.rh_contratacion_formadores.ver')
        kwargs['permiso_lideres'] = self.request.user.has_perm('permisos_sican.rh.rh_contratacion_lideres.ver')
        kwargs['permiso_negociadores'] = self.request.user.has_perm('permisos_sican.rh.rh_contratacion_negociadores.ver')
        return super(ContratacionView,self).get_context_data(**kwargs)

#--------------------------------------------- 2.1.1 FORMADORES --------------------------------------------------------

class ContratosFormadoresGeneralView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'rh/contratacion/contratos_formadores/lista_general.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.informes')
        return super(ContratosFormadoresGeneralView, self).get_context_data(**kwargs)

class ContratosFormadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de formadores y cantidad de contratos de cada uno
    '''
    template_name = 'rh/contratacion/contratos_formadores/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.informes')
        return super(ContratosFormadoresView, self).get_context_data(**kwargs)

class ContratoFormadorView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada al listado de contratos de cada formador.
    '''
    template_name = 'rh/contratacion/contratos_formadores/lista_contratos.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_formadores.informes')
        kwargs['formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        return super(ContratoFormadorView, self).get_context_data(**kwargs)

class NuevoContratoFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    '''
    Vista para la creacion de un nuevo contrato para el formador
    '''
    model = ContratoFormador
    form_class = ContratoFormadorForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_formadores/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.crear"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        return super(NuevoContratoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador']}

class UpdateContratoFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              UpdateView):
    '''
    Vista para actualizar el contrato de un formador
    '''
    model = ContratoFormador
    form_class = ContratoFormadorForm
    pk_url_kwarg = 'id_contrato'
    success_url = '../../'
    template_name = 'rh/contratacion/contratos_formadores/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['formador'] = Formador.objects.get(id = self.kwargs['id_formador']).get_full_name()
        kwargs['id_formador'] = self.kwargs['id_formador']
        kwargs['nombre_contrato'] = ContratoFormador.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(UpdateContratoFormadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_formador':self.kwargs['id_formador']}


class CohortesFormadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''

    '''
    template_name = 'rh/contratacion/contratos_formadores/cohortes/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver",
                "permisos_sican.rh.rh_cohortes_formadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_cohortes_formadores.informes')
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_cohortes_formadores.crear')
        return super(CohortesFormadoresView, self).get_context_data(**kwargs)

class CohortesFormadoresNuevoView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    '''
    Vista para la creacion de un nuevo contrato para el formador
    '''
    model = CohortesFormadores
    form_class = CohortesFormadoresForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_formadores/cohortes/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_contratos_formadores.ver",
                "permisos_sican.rh.rh_cohortes_formadores.ver",
                "permisos_sican.rh.rh_cohortes_formadores.crear"),
        "any": ()
    }

    def form_valid(self, form):
        self.object = form.save()
        cohorte_formadores.delay(self.object.id)
        return super(CohortesFormadoresNuevoView, self).form_valid(form)


#------------------------------------- 2.1.2 SOLICITUD SOPORTES FORMADORES ---------------------------------------------

class SolicitudSoportesFormadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/solicitud_soportes_formadores/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_formadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_formadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_formadores.informes')

        return super(SolicitudSoportesFormadoresView, self).get_context_data(**kwargs)

class NuevaSolicitudSoportesFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = SolicitudSoportesFormador
    form_class = SolicitudSoportesFormadorForm
    success_url = '../'
    template_name = 'rh/contratacion/solicitud_soportes_formadores/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_formadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_formadores.crear"),
        "any": ()
    }

class UpdateSolicitudSoportesFormadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              UpdateView):
    model = SolicitudSoportesFormador
    form_class = SolicitudSoportesFormadorForm
    pk_url_kwarg = 'id_solicitud_soporte'
    success_url = '../../'
    template_name = 'rh/contratacion/solicitud_soportes_formadores/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_formadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_formadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_formadores.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre'] = SolicitudSoportesFormador.objects.get(id=self.kwargs['id_solicitud_soporte']).nombre
        return super(UpdateSolicitudSoportesFormadorView, self).get_context_data(**kwargs)

#----------------------------------------------- 2.2.1 LIDERES ---------------------------------------------------------

class ContratosLideresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada a la lista de lideres y cantidad de contratos de cada uno
    '''
    template_name = 'rh/contratacion/contratos_lideres/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_contratos_lideres.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_lideres.informes')
        return super(ContratosLideresView, self).get_context_data(**kwargs)

class ContratoLiderView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    '''
    DatatableView enlazada al listado de contratos de cada lider.
    '''
    template_name = 'rh/contratacion/contratos_lideres/lista_contratos.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_contratos_lideres.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_lideres.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_lideres.informes')
        kwargs['lider'] = Lideres.objects.get(id = self.kwargs['id_lider']).get_full_name()
        kwargs['id_lider'] = self.kwargs['id_lider']
        return super(ContratoLiderView, self).get_context_data(**kwargs)

class NuevoContratoLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    '''
    Vista para la creacion de un nuevo contrato para el lider
    '''
    model = ContratoLider
    form_class = ContratoLiderForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_lideres/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_contratos_lideres.ver",
                "permisos_sican.rh.rh_contratos_lideres.crear"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['lider'] = Lideres.objects.get(id = self.kwargs['id_lider']).get_full_name()
        kwargs['id_lider'] = self.kwargs['id_lider']
        return super(NuevoContratoLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_lider':self.kwargs['id_lider']}

class UpdateContratoLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              UpdateView):
    '''
    Vista para actualizar el contrato de un lider
    '''
    model = ContratoLider
    form_class = ContratoLiderForm
    pk_url_kwarg = 'id_contrato'
    success_url = '../../'
    template_name = 'rh/contratacion/contratos_lideres/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_contratos_lideres.ver",
                "permisos_sican.rh.rh_contratos_lideres.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['lider'] = Lideres.objects.get(id = self.kwargs['id_lider']).get_full_name()
        kwargs['id_lider'] = self.kwargs['id_lider']
        kwargs['nombre_contrato'] = ContratoFormador.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(UpdateContratoLiderView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_lider':self.kwargs['id_lider']}

#--------------------------------------- 2.2.2 SOLICITUD SOPORTES LIDERES ----------------------------------------------

class SolicitudSoportesLideresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/solicitud_soportes_lideres/lista.html'
    permission_required = "permisos_sican.rh.solicitud_soportes_lideres.ver"
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_solicitud_soportes_lideres.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_lideres.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_lideres.informes')

        return super(SolicitudSoportesLideresView, self).get_context_data(**kwargs)

class NuevaSolicitudSoportesLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = SolicitudSoportesLider
    form_class = SolicitudSoportesLiderForm
    success_url = '../'
    template_name = 'rh/contratacion/solicitud_soportes_lideres/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_solicitud_soportes_lideres.ver",
                "permisos_sican.rh.rh_solicitud_soportes_lideres.crear"),
        "any": ()
    }

class UpdateSolicitudSoportesLiderView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              UpdateView):
    model = SolicitudSoportesLider
    form_class = SolicitudSoportesLiderForm
    pk_url_kwarg = 'id_solicitud_soporte'
    success_url = '../../'
    template_name = 'rh/contratacion/solicitud_soportes_lideres/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_lideres.ver",
                "permisos_sican.rh.rh_solicitud_soportes_lideres.ver",
                "permisos_sican.rh.rh_solicitud_soportes_lideres.editar"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['nombre'] = SolicitudSoportesLider.objects.get(id=self.kwargs['id_solicitud_soporte']).nombre
        return super(UpdateSolicitudSoportesLiderView, self).get_context_data(**kwargs)

#--------------------------------------------- 2.3.1 NEGOCIADORES ------------------------------------------------------

class ContratosNegociadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/contratos_negociadores/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_contratos_negociadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_negociadores.informes')
        return super(ContratosNegociadoresView, self).get_context_data(**kwargs)

class ContratoNegociadorView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/contratos_negociadores/lista_contratos.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_contratos_negociadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_negociadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_contratos_negociadores.informes')
        kwargs['negociador'] = Negociador.objects.get(id = self.kwargs['id_negociador']).get_full_name()
        kwargs['id_negociador'] = self.kwargs['id_negociador']
        return super(ContratoNegociadorView, self).get_context_data(**kwargs)

class NuevoContratoNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = ContratoNegociador
    form_class = ContratoNegociadorForm
    success_url = '../'
    template_name = 'rh/contratacion/contratos_negociadores/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_contratos_negociadores.ver",
                "permisos_sican.rh.rh_contratos_negociadores.crear"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['negociador'] = Negociador.objects.get(id = self.kwargs['id_negociador']).get_full_name()
        kwargs['id_negociador'] = self.kwargs['id_negociador']
        return super(NuevoContratoNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_negociador':self.kwargs['id_negociador']}

class UpdateContratoNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              UpdateView):
    model = ContratoNegociador
    form_class = ContratoNegociadorForm
    pk_url_kwarg = 'id_contrato'
    success_url = '../../'
    template_name = 'rh/contratacion/contratos_negociadores/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_contratos_negociadores.ver",
                "permisos_sican.rh.rh_contratos_negociadores.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['negociador'] = Negociador.objects.get(id = self.kwargs['id_negociador']).get_full_name()
        kwargs['id_negociador'] = self.kwargs['id_negociador']
        kwargs['nombre_contrato'] = ContratoNegociador.objects.get(id = self.kwargs['id_contrato']).nombre
        return super(UpdateContratoNegociadorView, self).get_context_data(**kwargs)

    def get_initial(self):
        return {'id_negociador':self.kwargs['id_negociador']}

#------------------------------------- 2.3.2 SOLICITUD SOPORTES NEGOCIADORES -------------------------------------------

class SolicitudSoportesNegociadoresView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'rh/contratacion/solicitud_soportes_negociadores/lista.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_negociadores.ver"),
        "any": ()
    }

    def get_context_data(self, **kwargs):
        kwargs['crear'] = self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_negociadores.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.rh.rh_solicitud_soportes_negociadores.informes')

        return super(SolicitudSoportesNegociadoresView, self).get_context_data(**kwargs)

class NuevaSolicitudSoportesNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              CreateView):
    model = SolicitudSoportesNegociador
    form_class = SolicitudSoportesNegociadorForm
    success_url = '../'
    template_name = 'rh/contratacion/solicitud_soportes_negociadores/nuevo.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_negociadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_negociadores.crear"),
        "any": ()
    }

class UpdateSolicitudSoportesNegociadorView(LoginRequiredMixin,
                              MultiplePermissionsRequiredMixin,
                              UpdateView):
    model = SolicitudSoportesNegociador
    form_class = SolicitudSoportesNegociadorForm
    pk_url_kwarg = 'id_solicitud_soporte'
    success_url = '../../'
    template_name = 'rh/contratacion/solicitud_soportes_negociadores/editar.html'
    permissions = {
        "all": ("permisos_sican.rh.rh_contratacion.ver",
                "permisos_sican.rh.rh_contratacion_negociadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_negociadores.ver",
                "permisos_sican.rh.rh_solicitud_soportes_negociadores.editar"),
        "any": ()
    }


    def get_context_data(self, **kwargs):
        kwargs['nombre'] = SolicitudSoportesNegociador.objects.get(id=self.kwargs['id_solicitud_soporte']).nombre
        return super(UpdateSolicitudSoportesNegociadorView, self).get_context_data(**kwargs)

#-----------------------------------------------------------------------------------------------------------------------



class ListaRequerimientosContratacionView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/requerimientosrh/lista.html'
    permission_required = "permisos_sican.rh.requerimientosrhrespuesta.ver"

    def get_context_data(self, **kwargs):
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.requerimientosrhrespuesta.reportes')
        return super(ListaRequerimientosContratacionView, self).get_context_data(**kwargs)

class NuevoRequerimientoContratacionView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = RequerimientoPersonal
    form_class = RequerimientoPersonalRh
    form_class_2 = RequerimientoPersonalRhEspera
    form_class_3 = RequerimientoPersonalRhContratar
    form_class_4 = RequerimientoPersonalRhDeserta
    pk_url_kwarg = 'pk'
    success_url = '/rh/requerimientoscontratacion/'
    template_name = 'rh/requerimientosrh/editar.html'
    permission_required = "permisos_sican.rh.requerimientosrhrespuesta.editar"

    def get_form_class(self):
        obj = RequerimientoPersonal.objects.get(id = self.kwargs['pk'])

        if obj.remitido_respuesta == True and obj.remitido_contratacion == False and obj.contratar == False and obj.desierto == False and obj.contratado == False:
            return self.form_class_2
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == True and obj.desierto == False and obj.contratado == False:
            return self.form_class_3
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == False and obj.desierto == True and obj.contratado == False:
            return self.form_class_4
        elif obj.contratado == True:
            return self.form_class_3
        else:
            return self.form_class

    def get_context_data(self, **kwargs):
        kwargs['link_old_file'] = self.object.get_archivo_url()
        kwargs['old_file'] = self.object.archivo_filename()
        return super(NuevoRequerimientoContratacionView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        obj = self.object

        if obj.remitido_respuesta == True and obj.remitido_contratacion == False and obj.contratar == False and obj.desierto == False and obj.contratado == False:
            pass
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == True and obj.desierto == False and obj.contratado == False:
            pass
        elif obj.remitido_respuesta == True and obj.remitido_contratacion == True and obj.contratar == False and obj.desierto == True and obj.contratado == False:
            pass
        elif obj.contratado == True:
            pass
        else:
            self.object.remitido_respuesta = True
            self.object.fecha_respuesta = datetime.datetime.now()
            self.object.save()
            destinatarios = [self.object.solicitante,self.object.encargado]

            url_base = self.request.META['HTTP_ORIGIN']
            for destinatario in list(set(destinatarios)):
                send_mail_templated.delay('email/requerimiento_contratacion_rh.tpl', {'id_requerimiento':self.object.id,
                                                                                  'first_name': destinatario.first_name,
                                                                                  'last_name': destinatario.last_name,
                                                                                  'url_base': url_base,
                                                                    }, DEFAULT_FROM_EMAIL, [destinatario.email])

        return super(NuevoRequerimientoContratacionView, self).form_valid(form)


class FormadoresConsolidadoView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'rh/interventoria_formadores/lista.html'
    permission_required = "permisos_sican.rh.interventoria_formadores.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.crear')
        kwargs['masivo_permiso'] = self.request.user.has_perm('permisos_sican.rh.formadores.masivo')
        return super(FormadoresConsolidadoView, self).get_context_data(**kwargs)