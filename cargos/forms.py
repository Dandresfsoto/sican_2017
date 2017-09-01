#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from administrativos.models import Administrativo
from cargos.models import Cargo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML

class NuevoCargoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoCargoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Cargo',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        HTML("""
                            <file-upload-sican name="manual">Manual</file-upload-sican>
                        """),
                        css_class='col-sm-12'
                    ),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Cargo
        fields = '__all__'

class EditarCargoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditarCargoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Cargo',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div(
                        HTML("""
                            <file-upload-sican name="manual" old_file="{{manual_filename}}" link_old_file="{{manual_link}}">Manual</file-upload-sican>
                        """),
                        css_class='col-sm-12'
                    ),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Cargo
        fields = '__all__'