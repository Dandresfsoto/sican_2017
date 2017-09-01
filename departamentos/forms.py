#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from departamentos.models import Departamento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML



class DepartamentoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Departamento',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codigo_departamento',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codigo_pais',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codigo_auditoria',css_class='col-sm-12'),
                    css_class = 'row'
                )
            )
        )

    class Meta:
        model = Departamento
        fields = '__all__'