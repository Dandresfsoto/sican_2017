#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from productos.models import Diplomado, Nivel, Sesion
from productos.forms import DiplomadoForm, UpdateDiplomadoForm, NivelForm, UpdateNivelForm, SesionForm, UpdateSesionForm
from productos.forms import EntregableForm, UpdateEntregableForm
from productos.models import Entregable

# Create your views here.

class DiplomadosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'productos/diplomados/lista.html'
    permission_required = "permisos_sican.productos.diplomados.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.productos.diplomados.crear')
        return super(DiplomadosListView, self).get_context_data(**kwargs)


class DiplomadoCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Diplomado
    form_class = DiplomadoForm
    success_url = '/estrategia/diplomados/'
    template_name = 'productos/diplomados/nuevo.html'
    permission_required = "permisos_sican.productos.diplomados.crear"


class DiplomadoUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Diplomado
    form_class = UpdateDiplomadoForm
    pk_url_kwarg = 'pk'
    success_url = '/estrategia/diplomados/'
    template_name = 'productos/diplomados/editar.html'
    permission_required = "permisos_sican.productos.diplomados.editar"




class NivelesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'productos/niveles/lista.html'
    permission_required = "permisos_sican.productos.niveles.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.productos.niveles.crear')
        return super(NivelesListView, self).get_context_data(**kwargs)


class NivelesCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Nivel
    form_class = NivelForm
    success_url = '/estrategia/niveles/'
    template_name = 'productos/niveles/nuevo.html'
    permission_required = "permisos_sican.productos.niveles.crear"


class NivelesUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Nivel
    form_class = UpdateNivelForm
    pk_url_kwarg = 'pk'
    success_url = '/estrategia/niveles/'
    template_name = 'productos/niveles/editar.html'
    permission_required = "permisos_sican.productos.niveles.editar"



class SesionesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'productos/sesiones/lista.html'
    permission_required = "permisos_sican.productos.sesiones.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.productos.sesiones.crear')
        return super(SesionesListView, self).get_context_data(**kwargs)


class SesionesCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Sesion
    form_class = SesionForm
    success_url = '/estrategia/sesiones/'
    template_name = 'productos/sesiones/nuevo.html'
    permission_required = "permisos_sican.productos.sesiones.crear"


class SesionesUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Sesion
    form_class = UpdateSesionForm
    pk_url_kwarg = 'pk'
    success_url = '/estrategia/sesiones/'
    template_name = 'productos/sesiones/editar.html'
    permission_required = "permisos_sican.productos.sesiones.editar"



class EntregablesListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'productos/entregables/lista.html'
    permission_required = "permisos_sican.productos.entregables.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.productos.entregables.crear')
        return super(EntregablesListView, self).get_context_data(**kwargs)


class EntregablesCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               CreateView):
    model = Entregable
    form_class = EntregableForm
    success_url = '/estrategia/entregables/'
    template_name = 'productos/entregables/nuevo.html'
    permission_required = "permisos_sican.productos.entregables.crear"

class EntregablesUpdateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Entregable
    form_class = UpdateEntregableForm
    pk_url_kwarg = 'pk'
    success_url = '/estrategia/entregables/'
    template_name = 'productos/entregables/editar.html'
    permission_required = "permisos_sican.productos.entregables.editar"

    def get_context_data(self, **kwargs):
        kwargs['old_file'] = self.object.archivo_filename()
        kwargs['link_old_file'] = self.object.get_archivo_url()
        return super(EntregablesUpdateView,self).get_context_data(**kwargs)
