#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from matrices.models import Beneficiario
from matrices.forms import BeneficiarioForm, BeneficiarioUpdateForm
from radicados.models import Radicado
from matrices.models import CargaMasiva
from matrices.forms import CargaMasivaForm
from matrices.tasks import carga_masiva_matrices


# Create your views here.
class ListadoMatricesView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'matrices/diplomados/lista.html'
    permissions = {
        "any": ("permisos_sican.matrices.matricesdiplomados.ver_innovatic", "permisos_sican.matrices.matricesdiplomados.ver_tecnotic",
                "permisos_sican.matrices.matricesdiplomados.ver_directic", "permisos_sican.matrices.matricesdiplomados.ver_escuelatic")
    }

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.matrices.matricesdiplomados.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.matrices.matricesdiplomados.informes')
        kwargs['diplomado'] = kwargs['diplomado'].upper()
        return super(ListadoMatricesView, self).get_context_data(**kwargs)


class NuevoBeneficiarioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Beneficiario
    form_class = BeneficiarioForm
    success_url = '../'
    template_name = 'matrices/diplomados/nuevo.html'
    permission_required = "permisos_sican.matrices.matricesdiplomados.crear"

    def get_initial(self):
        return {'diplomado_nombre':self.kwargs['diplomado'].upper()}

    def get_context_data(self, **kwargs):
        kwargs['diplomado'] = self.kwargs['diplomado'].upper()
        return super(NuevoBeneficiarioView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.object.diplomado.nombre != 'ESCUELA TIC FAMILIA':
            self.object.radicado = Radicado.objects.get(numero=form.cleaned_data['radicado_text'])
        self.object.save()
        return super(NuevoBeneficiarioView, self).form_valid(form)


class UpdateBeneficiarioView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Beneficiario
    form_class = BeneficiarioUpdateForm
    success_url = '../../'
    template_name = 'matrices/diplomados/editar.html'
    permission_required = "permisos_sican.matrices.matricesdiplomados.editar"

    def get_initial(self):
        return {'diplomado_nombre':self.kwargs['diplomado'].upper(),'formador_id':self.object.formador.id,'beneficiario_id':self.object.id}

    def get_context_data(self, **kwargs):
        kwargs['diplomado'] = self.kwargs['diplomado'].upper()
        return super(UpdateBeneficiarioView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.object.diplomado.nombre != 'ESCUELA TIC FAMILIA':
            self.object.radicado = Radicado.objects.get(numero=form.cleaned_data['radicado_text'])
        self.object.save()
        return super(UpdateBeneficiarioView, self).form_valid(form)


class DeleteBeneficiarioView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Beneficiario
    pk_url_kwarg = 'pk'
    success_url = '../../'
    template_name = 'matrices/diplomados/eliminar.html'
    permission_required = "permisos_sican.matrices.matricesdiplomados.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['diplomado'] = self.kwargs['diplomado'].upper()
        return super(DeleteBeneficiarioView, self).get_context_data(**kwargs)





class ListadoCargasMasivasView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'matrices/cargamasiva/lista.html'
    permission_required = "permisos_sican.matrices.cargamasiva.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.matrices.cargamasiva.crear')
        return super(ListadoCargasMasivasView, self).get_context_data(**kwargs)


class NuevaCargaMasiva(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = CargaMasiva
    form_class = CargaMasivaForm
    success_url = '../'
    template_name = 'matrices/cargamasiva/nuevo.html'
    permission_required = "permisos_sican.matrices.cargamasiva.crear"

    def get_initial(self):
        return {'id_usuario':self.request.user.id}

    def form_valid(self, form):
        self.object = form.save()
        carga_masiva_matrices.delay(self.object.id,self.request.user.email)
        return super(NuevaCargaMasiva,self).form_valid(form)