#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from rh.models import TipoSoporte
from productos.models import Diplomado, Nivel, Sesion, Entregable
from productos.models import Contratos

class DiplomadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DiplomadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Nuevo diplomado',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Diplomado
        fields = '__all__'

class UpdateDiplomadoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateDiplomadoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Editar diplomado',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Diplomado
        fields = '__all__'

class NivelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NivelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Nuevo nivel',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('diplomado',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Nivel
        fields = '__all__'

class UpdateNivelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateNivelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Editar nivel',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('diplomado',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Nivel
        fields = '__all__'

class SesionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SesionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Nueva sesión',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('nivel',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Sesion
        fields = '__all__'

class UpdateSesionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateSesionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Editar sesión',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('nivel',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Sesion
        fields = '__all__'

class EntregableForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EntregableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Nuevo entregable',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('sesion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('tipo',css_class='col-sm-6'),
                    Div('escencial',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="formato">Formato</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Entregable
        fields = '__all__'
        widgets = {
            'tipo':forms.Select(choices=(('Virtual','Virtual',),('Presencial','Presencial'))),
            'escencial':forms.Select(choices=(('No','No',),('Si','Si')))
        }

class UpdateEntregableForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateEntregableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Editar entregable',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('numero',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('sesion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('tipo',css_class='col-sm-6'),
                    Div('escencial',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="formato" old_file="{{old_file}}"
                            link_old_file="{{link_old_file}}">Formato</file-upload-sican>
                        """),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = Entregable
        fields = '__all__'

        widgets = {
            'tipo':forms.Select(choices=(('Virtual','Virtual',),('Presencial','Presencial'))),
            'escencial':forms.Select(choices=(('No','No',),('Si','Si')))
        }

class ContratosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContratosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Contrato',
                Div(
                    Div('nombre',css_class='col-sm-6'),
                    Div('cargo',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Contratos
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(),
        }