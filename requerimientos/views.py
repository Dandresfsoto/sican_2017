#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from requerimientos.forms import RequerimientoForm
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from requerimientos.models import Requerimiento
from requerimientos.tasks import send_mail_templated_requerimiento
from sican.settings.base import DEFAULT_FROM_EMAIL
import locale

class RequerimientosListView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = 'requerimientos/interventoria/lista.html'
    permission_required = "permisos_sican.requerimientos.proyecto.ver"

    def get_context_data(self, **kwargs):
        kwargs['nuevo_permiso'] = self.request.user.has_perm('permisos_sican.requerimientos.proyecto.crear')
        return super(RequerimientosListView, self).get_context_data(**kwargs)


class NuevoRequerimientoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              CreateView):
    model = Requerimiento
    form_class = RequerimientoForm
    success_url = '/requerimientos/delegacion/'
    template_name = 'requerimientos/interventoria/nuevo.html'
    permission_required = "permisos_sican.requerimientos.proyecto.crear"

    def form_valid(self, form):
        self.object = form.save()
        url_base = self.request.META['HTTP_ORIGIN']
        send_mail_templated_requerimiento.delay('email/requerimiento.tpl', {'url_base':url_base,
                                                                            'nombre_requerimiento':self.object.nombre,
                                                                            'fecha_solicitud':self.object.recepcion_solicitud.strftime('%d/%m/%Y'),
                                                                            'entidad_remitente':self.object.entidad_remitente,
                                                                            'funcionario':self.object.funcionario_remitente,
                                                                            'archivo_url':url_base + self.object.get_archivo_solicitud_url(),
                                                                            'descripcion':self.object.descripcion,
                                                                            'plazo':self.object.tiempo_respuesta,
                                                                            'encargados':self.object.get_encargados_string(),
                                                                            'medio_entrega':self.object.medio_entrega,
                                                                            },
                                                DEFAULT_FROM_EMAIL,
                                                list(self.object.encargados.values_list('email',flat=True)))
        return super(NuevoRequerimientoView,self).form_valid(form)


class UpdateRequerimientoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              UpdateView):
    model = Requerimiento
    form_class = RequerimientoForm
    success_url = '/requerimientos/delegacion/'
    template_name = 'requerimientos/interventoria/editar.html'
    permission_required = "permisos_sican.requerimientos.proyecto.editar"


class DeleteRequerimientoView(LoginRequiredMixin,
                              PermissionRequiredMixin,
                              DeleteView):
    model = Requerimiento
    success_url = '/requerimientos/delegacion/'
    template_name = 'requerimientos/interventoria/eliminar.html'
    permission_required = "permisos_sican.requerimientos.proyecto.editar"