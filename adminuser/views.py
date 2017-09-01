#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from usuarios.models import User
from usuarios.forms import UserUpdateAdminForm, UserNewAdminForm, GroupNewAdminForm, NuevoPermisoForm
from usuarios.tasks import send_mail_templated
from sican.settings.base import DEFAULT_FROM_EMAIL
from django.shortcuts import HttpResponseRedirect
import random
import string
from django.contrib.auth.models import Group, Permission
# Create your views here.

class UserListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'adminuser/usuarios/lista.html'
    permission_required = "permisos_sican.adminuser.usuarios.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.adminuser.usuarios.crear')
        return super(UserListView, self).get_context_data(**kwargs)

class UpdateUserView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = User
    form_class = UserUpdateAdminForm
    pk_url_kwarg = 'pk'
    success_url = '/adminuser/usuarios/'
    template_name = 'adminuser/usuarios/editar.html'
    permission_required = "permisos_sican.adminuser.usuarios.editar"

    def form_valid(self, form):
        form.save()
        user = User.objects.get(email=self.object.email)
        user.fullname = user.first_name + " " + user.last_name
        user.save()
        return HttpResponseRedirect('/adminuser/usuarios/')

class NewUserView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = User
    form_class = UserNewAdminForm
    success_url = '/adminuser/usuarios/'
    template_name = 'adminuser/usuarios/nuevo.html'
    permission_required = "permisos_sican.adminuser.usuarios.crear"

    def form_valid(self, form):
        form.save()
        user = User.objects.get(email=form.data['email'])
        user.fullname = user.first_name + " " + user.last_name
        user.save()

        password = "".join([random.choice(string.ascii_letters) for i in xrange(6)])
        user.set_password(password)
        user.save()
        send_mail_templated.delay('email/new_user.tpl',
                                  {'url_base' : self.request.META['HTTP_ORIGIN'],'first_name': user.first_name, 'last_name': user.last_name,
                                   'email': user.email, 'password':password},
                                  DEFAULT_FROM_EMAIL,[form.data['email']])
        return HttpResponseRedirect('/adminuser/usuarios/')

class GroupListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'adminuser/grupos/lista.html'
    permission_required = "permisos_sican.adminuser.grupos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.adminuser.grupos.crear')
        return super(GroupListView, self).get_context_data(**kwargs)

class NewGroupView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Group
    form_class = GroupNewAdminForm
    success_url = '/adminuser/grupos/'
    template_name = 'adminuser/grupos/nuevo.html'
    permission_required = "permisos_sican.adminuser.grupos.crear"

class UpdateGrupoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UpdateView):
    model = Group
    form_class = GroupNewAdminForm
    pk_url_kwarg = 'pk'
    success_url = '/adminuser/grupos/'
    template_name = 'adminuser/grupos/editar.html'
    permission_required = "permisos_sican.adminuser.grupos.editar"


class DeleteGrupoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Group
    pk_url_kwarg = 'pk'
    success_url = '/adminuser/grupos/'
    template_name = 'adminuser/grupos/eliminar.html'
    permission_required = "permisos_sican.adminuser.grupos.eliminar"

    def get_context_data(self, **kwargs):
        kwargs['nombre_grupo'] = self.object.name
        result = []
        permisos = Group.objects.get(id=self.object.id).permissions.all()
        for permiso in permisos:
            result.append(permiso.__str__())
        kwargs['permisos'] = result
        return super(DeleteGrupoView, self).get_context_data(**kwargs)

class PermisosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'adminuser/permisos/lista.html'
    permission_required = "permisos_sican.adminuser.permisos.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.adminuser.permisos.ver')
        return super(PermisosListView, self).get_context_data(**kwargs)

class NuevoPermisoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Permission
    form_class = NuevoPermisoForm
    success_url = '/adminuser/permisos/'
    template_name = 'adminuser/permisos/nuevo.html'
    permission_required = "permisos_sican.adminuser.permisos.crear"

class EditarPermisoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Permission
    form_class = NuevoPermisoForm
    pk_url_kwarg = 'pk'
    success_url = '/adminuser/permisos/'
    template_name = 'adminuser/permisos/editar.html'
    permission_required = "permisos_sican.adminuser.permisos.editar"

class EliminarPermisoView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               DeleteView):
    model = Permission
    pk_url_kwarg = 'pk'
    success_url = '/adminuser/permisos/'
    template_name = 'adminuser/permisos/eliminar.html'
    permission_required = "permisos_sican.adminuser.permisos.eliminar"