#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, FormView, View
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from django.shortcuts import render
from beneficiarios.models import GruposBeneficiarios, BeneficiarioVigencia
from beneficiarios.forms import GruposBeneficiariosForm, BeneficiarioVigenciaForm
from django.shortcuts import redirect

# Create your views here.

# Create your views here.
class ListaBeneficiariosView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'beneficiarios/registrar/lista.html'
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",)
    }

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.informes')
        return super(ListaBeneficiariosView, self).get_context_data(**kwargs)


class NuevoGrupoView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         CreateView):
    model = GruposBeneficiarios
    form_class = GruposBeneficiariosForm
    success_url = '../'
    template_name = 'beneficiarios/registrar/nuevo_grupo.html'
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",
                "permisos_sican.beneficiarios.beneficiarios_registrar.crear")
    }

    def get_initial(self):
        return {'user':self.request.user}


class UpdateGrupoView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         UpdateView):
    pk_url_kwarg = 'id_grupo'
    model = GruposBeneficiarios
    form_class = GruposBeneficiariosForm
    success_url = '../../../'
    template_name = 'beneficiarios/registrar/editar_grupo.html'
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",
                "permisos_sican.beneficiarios.beneficiarios_registrar.editar")
    }

    def get_initial(self):
        return {'user':self.request.user}

    def get_context_data(self, **kwargs):
        kwargs['nombre_grupo'] = self.object.nombre
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        return super(UpdateGrupoView,self).get_context_data(**kwargs)


class ListaBeneficiariosGrupoView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         TemplateView):
    template_name = 'beneficiarios/registrar/lista_beneficiarios_grupo.html'
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",
                "permisos_sican.beneficiarios.beneficiarios_registrar.crear")
    }

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.crear')
        kwargs['informes'] = self.request.user.has_perm('permisos_sican.beneficiarios.beneficiarios_registrar.informes')
        kwargs['nombre_grupo'] = GruposBeneficiarios.objects.get(id = self.kwargs['id_grupo']).nombre
        kwargs['id_grupo'] = self.kwargs['id_grupo']
        return super(ListaBeneficiariosGrupoView, self).get_context_data(**kwargs)



class NuevoBeneficiarioView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         CreateView):
    model = BeneficiarioVigencia
    form_class = BeneficiarioVigenciaForm
    success_url = '../'
    template_name = 'beneficiarios/registrar/nuevo_beneficiario.html'
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",
                "permisos_sican.beneficiarios.beneficiarios_registrar.crear")
    }

    def get_initial(self):
        return {'grupo':GruposBeneficiarios.objects.get(id=self.kwargs['id_grupo'])}

    def get_context_data(self, **kwargs):
        kwargs['nombre_grupo'] = GruposBeneficiarios.objects.get(id=self.kwargs['id_grupo']).nombre
        return super(NuevoBeneficiarioView, self).get_context_data(**kwargs)


class UpdateEstadoBeneficiarioView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         View):
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",
                "permisos_sican.beneficiarios.beneficiarios_registrar.crear")
    }

    def dispatch(self, request, *args, **kwargs):
        try:
            beneficiario = BeneficiarioVigencia.objects.get(id=kwargs['id_beneficiario'])
        except:
            pass
        else:
            if beneficiario.estado == 'Activo':
                beneficiario.estado = 'Inactivo'
            else:
                beneficiario.estado = 'Activo'
            beneficiario.save()
        return redirect('../../')



class UpdateBeneficiarioView(LoginRequiredMixin,
                         MultiplePermissionsRequiredMixin,
                         UpdateView):
    pk_url_kwarg = 'id_beneficiario'
    model = BeneficiarioVigencia
    form_class = BeneficiarioVigenciaForm
    success_url = '../../'
    template_name = 'beneficiarios/registrar/editar_beneficiario.html'
    permissions = {
        "any": ("permisos_sican.beneficiarios.beneficiarios_registrar.ver",
                "permisos_sican.beneficiarios.beneficiarios_registrar.editar")
    }

    def get_initial(self):
        return {'grupo':GruposBeneficiarios.objects.get(id=self.kwargs['id_grupo'])}

    def get_context_data(self, **kwargs):
        kwargs['nombre_grupo'] = GruposBeneficiarios.objects.get(id=self.kwargs['id_grupo']).nombre
        return super(UpdateBeneficiarioView,self).get_context_data(**kwargs)