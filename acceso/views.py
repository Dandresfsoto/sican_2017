#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from radicados.models import RadicadoRetoma
from radicados.forms import RadicadoRetomaForm
from acceso.models import Retoma
from acceso.forms import RetomaForm



class ListaRadicadosRetomaView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'acceso/radicadosretoma/lista.html'
    permission_required = "permisos_sican.acceso.radicadosretoma.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.acceso.radicadosretoma.crear')
        return super(ListaRadicadosRetomaView, self).get_context_data(**kwargs)


class NuevoRadicadosRetomaView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = RadicadoRetoma
    form_class = RadicadoRetomaForm
    success_url = '/acceso/radicadosretoma/'
    template_name = 'acceso/radicadosretoma/nuevo.html'
    permission_required = "permisos_acceso.radicadosretoma.crear"


class UpdateRadicadosRetomaView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = RadicadoRetoma
    form_class = RadicadoRetomaForm
    pk_url_kwarg = 'pk'
    success_url = '/acceso/radicadosretoma/'
    template_name = 'acceso/radicadosretoma/editar.html'
    permission_required = "permisos_acceso.radicadosretoma.editar"


class DeleteRadicadosRetomaView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = RadicadoRetoma
    form_class = RadicadoRetomaForm
    pk_url_kwarg = 'pk'
    success_url = '/acceso/radicadosretoma/'
    template_name = 'acceso/radicadosretoma/eliminar.html'
    permission_required = "permisos_acceso.radicadosretoma.eliminar"




class ListaRetomaView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'acceso/retoma/lista.html'
    permission_required = "permisos_sican.acceso.retoma.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.acceso.retoma.crear')
        return super(ListaRetomaView, self).get_context_data(**kwargs)


class NuevaRetomaView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Retoma
    form_class = RetomaForm
    success_url = '/acceso/retoma/'
    template_name = 'acceso/retoma/nuevo.html'
    permission_required = "permisos_acceso.retoma.crear"