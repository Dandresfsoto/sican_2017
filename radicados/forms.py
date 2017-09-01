#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from radicados.models import Radicado, RadicadoRetoma
from secretarias.models import Secretaria
from municipios.models import Municipio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML


class RadicadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RadicadoForm, self).__init__(*args, **kwargs)
        self.fields['secretaria'].queryset = Secretaria.objects.exclude(oculto = True)
        self.fields['municipio'].queryset = Municipio.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Radicado',
                Div(
                    Div('numero',css_class='col-sm-4'),
                    Div('secretaria',css_class='col-sm-4'),
                    Div('municipio',css_class='col-sm-4'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Institución Educativa',
                Div(
                    Div('nombre_ie',css_class='col-sm-4'),
                    Div('ie_id',css_class='col-sm-4'),
                    Div('dane_ie',css_class='col-sm-4'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Sede Educativa',
                Div(
                    Div('nombre_sede',css_class='col-sm-4'),
                    Div('sede_id',css_class='col-sm-4'),
                    Div('dane_sede',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('zona',css_class='col-sm-4'),
                    Div('matricula',css_class='col-sm-4'),
                    Div('direccion',css_class='col-sm-4'),
                    css_class = 'row'
                )
            )
        )

    class Meta:
        model = Radicado
        fields = '__all__'
        labels = {
            'nombre_ie':'Nombre',
            'dane_ie':'Código Dane',
            'ie_id':'ID',
            'nombre_sede':'Nombre',
            'dane_sede':'Código Dane',
            'sede_id':'ID',
            'direccion':'Dirección',
            'matricula':'Matrícula',
        }

class RadicadoRetomaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RadicadoRetomaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Radicado Retoma',
                Div(
                    Div('numero',css_class='col-sm-4'),
                    Div('municipio',css_class='col-sm-4'),
                    Div('ubicacion',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('institucion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('sede',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('nombre_completo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('dane',css_class='col-sm-12'),
                    css_class = 'row'
                )
            )
        )

    class Meta:
        model = RadicadoRetoma
        fields = '__all__'
        widgets = {
            'ubicacion' : forms.Select(choices=(('Rural','Rural'),('Urbana','Urbana')))
        }