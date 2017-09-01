#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from municipios.models import Municipio
from departamentos.models import Departamento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML



class MunicipioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MunicipioForm, self).__init__(*args, **kwargs)
        self.fields['departamento'].queryset = Departamento.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Municipio',
                Div(
                    Div('departamento',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codigo_auditoria',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codigo_municipio',css_class='col-sm-12'),
                    css_class = 'row'
                )
            )
        )

    class Meta:
        model = Municipio
        fields = '__all__'