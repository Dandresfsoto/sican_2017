#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from municipios.models import Municipio
from secretarias.models import Secretaria
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML



class SecretariaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SecretariaForm, self).__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Secretaría de educación',
                Div(
                    Div('municipio',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('tipo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('direccion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('web',css_class='col-sm-12'),
                    css_class = 'row'
                )
            )
        )

    class Meta:
        model = Secretaria
        fields = '__all__'