#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from celery import shared_task
from mail_templated import send_mail
from requerimientos.models import Requerimiento
from sican.settings.base import DEFAULT_FROM_EMAIL


@shared_task
def send_mail_templated_requerimiento(template,dictionary,from_email,list_to_email):
    send_mail(template, dictionary, from_email, list_to_email)
    return 'Email enviado'

@shared_task
def recordatorio_requerimiento():
    for requerimiento in Requerimiento.objects.all():
        if requerimiento.estado == 'Abierto':
            if requerimiento.get_dias_mora() > 0:
                estado = 'tiene ' + str(requerimiento.get_dias_mora()) + ' dia(s) en mora'
            else:
                estado = 'tiene un plazo de ' + str(abs(requerimiento.get_dias_mora())) + ' dia(s) para ser respondido,'

            url_base = 'https://sican.asoandes.org'

            send_mail_templated_requerimiento('email/requerimiento_recordatorio.tpl', {'url_base':url_base,
                                                                                    'estado':estado,
                                                                                    'nombre_requerimiento':requerimiento.nombre,
                                                                                    'fecha_solicitud':requerimiento.recepcion_solicitud.strftime('%d/%m/%Y'),
                                                                                    'entidad_remitente':requerimiento.entidad_remitente,
                                                                                    'funcionario':requerimiento.funcionario_remitente,
                                                                                    'archivo_url':url_base + requerimiento.get_archivo_solicitud_url(),
                                                                                    'descripcion':requerimiento.descripcion,
                                                                                    'plazo':requerimiento.tiempo_respuesta,
                                                                                    'encargados':requerimiento.get_encargados_string(),
                                                                                    'medio_entrega':requerimiento.medio_entrega,
                                                                                    },
                                                        DEFAULT_FROM_EMAIL,
                                                        list(requerimiento.encargados.values_list('email',flat=True)))
    return 'Email enviado'