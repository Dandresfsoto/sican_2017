#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from requerimientos.models import Requerimiento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML


class RequerimientoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Requerimiento',
                Div(
                    Div('recepcion_solicitud',css_class='col-sm-6'),
                    Div('region',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('entidad_remitente',css_class='col-sm-6'),
                    Div('funcionario_remitente',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('nombre',css_class='col-sm-6'),
                    Div('archivo_solicitud',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Delegación del requeerimiento',
                Div(
                    Div('tiempo_respuesta',css_class='col-sm-6'),
                    Div('medio_entrega',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('encargados',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Cierre del requerimiento',
                Div(
                    Div('estado',css_class='col-sm-3'),
                    Div('fecha_respuesta',css_class='col-sm-3'),
                    Div('archivo_respuesta',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('observaciones',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Requerimiento
        fields = '__all__'
        widgets = {
            'entidad_remitente': forms.Select(choices = ( ('','----------'),('Andes','Andes'),('CPE','CPE'),('Interventoria','Interventoria'),('Secretatia de educación','Secretatia de educación'),('Otros','Otros')) ),
            'estado': forms.Select(choices= ( ('Abierto','Abierto'),('Cerrado','Cerrado') )),
            'medio_entrega': forms.Select(choices= ( ('','----------'),('Archivo en fisico','Archivo en fisico'),('Correo electrónico','Correo electrónico') )),
        }
        labels = {
            'recepcion_solicitud': 'Fecha de solicitud',
            'entidad_remitente': 'Entidad remitente',
            'funcionario_remitente': 'Funcionario y/o eje',
            'nombre': 'Nombre del requerimiento',
            'archivo_solicitud': 'Archivo de la solicitud',
            'descripcion': 'Descripción',
            'tiempo_respuesta': 'Cantidad de dias para responder',
            'medio_entrega': 'Medio de entrega',
            'encargados': 'Encargados del requerimiento',
            'fecha_respuesta': 'Fecha de cierre',
            'archivo_respuesta': 'Archivo de la respuesta'
        }