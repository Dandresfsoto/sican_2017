#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from administrativos.models import Administrativo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from negociadores.models import Negociador, Soporte
from cargos.models import Cargo
from rh.models import TipoSoporte
from negociadores.models import Contrato
from negociadores.models import SolicitudSoportes

class NegociadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NegociadorForm, self).__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Usuario del sistema y Region',
                Div(
                    Div('usuario',css_class='col-sm-6'),
                    Div('region',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Datos personales',
                Div(
                    Div('nombres',css_class='col-sm-6'),
                    Div('apellidos',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('cedula',css_class='col-sm-4'),
                    Div('correo_personal',css_class='col-sm-4'),
                    Div('celular_personal',css_class='col-sm-4'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Información profesional',
                Div(
                    Div('cargo',css_class='col-sm-6'),
                    Div('profesion',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('fecha_contratacion',css_class='col-sm-6'),
                    Div('fecha_terminacion',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Seguridad social e información bancaria',
                Div(
                    Div('eps',css_class='col-sm-4'),
                    Div('pension',css_class='col-sm-4'),
                    Div('arl',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('banco',css_class='col-sm-4'),
                    Div('tipo_cuenta',css_class='col-sm-4'),
                    Div('numero_cuenta',css_class='col-sm-4'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Negociador
        fields = '__all__'
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ),
        }

class NuevoSoporteNegociadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoSoporteNegociadorForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoSoporte.objects.exclude(oculto = True)
        if 'data' in kwargs:
            kwargs['data']['negociador'] = kwargs['initial']['negociador']
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Soporte:',
                Div(
                    Div('fecha',css_class='col-sm-6'),
                    Div('tipo',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="archivo" old_file="{{old_file}}"
                            link_old_file="{{link_old_file}}">Archivo</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
                Div(
                    Div('administrativo',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = Soporte
        fields = '__all__'
        widgets = {
            'tipo': forms.Select()
        }

class ContratoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)

        self.fields['negociador'].initial = Negociador.objects.get(id = kwargs['initial']['id_negociador'])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información inicial de contrato',
                Div(
                    Div('nombre',css_class='col-sm-6'),
                    Div('soportes_requeridos',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('fecha_inicio',css_class='col-sm-6'),
                    Div('fecha_fin',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('negociador',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Soportes',
                Div(
                    Div('soporte_renuncia',css_class='col-sm-6'),
                    Div('soporte_liquidacion',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('renuncia',css_class='col-sm-6'),
                    Div('liquidado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Contrato
        fields = '__all__'
        widgets = {'negociador':forms.HiddenInput()}

class SolicitudSoportesNegociadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitudSoportesNegociadorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Solicitud de soportes',
                Div(
                    Div('nombre',css_class='col-sm-6'),
                    Div('soportes_requeridos',css_class='col-sm-6'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = SolicitudSoportes
        fields = '__all__'

class LegalizacionForm(forms.Form):

    ids = forms.CharField(max_length=200,required=False,widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(LegalizacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        contrato = Contrato.objects.get(id = kwargs['initial']['id_contrato'])
        ids = contrato.soportes_requeridos.soportes_requeridos.filter(categoria = 'General').values_list('id',flat=True)
        self.fields['ids'].initial = unicode(ids)

        self.helper.layout = Layout(
            Fieldset(
                'Documentos generales',
            ),
            Div('ids'),
            HTML(
                """
                <p>*Anexe todos los soportes digitales para la legalización del contrato, todos los campos con obligatorios.</p>
                """
            )
        )

        fields = []

        for soporte in contrato.soportes_requeridos.soportes_requeridos.filter(categoria = 'General'):

            tipo = TipoSoporte.objects.get(id = soporte.id)

            soporte_file = None

            try:
                soporte_file = Soporte.objects.get(contrato = contrato,negociador = contrato.negociador,tipo = tipo)
            except:
                pass

            self.fields[str(soporte.id)] = forms.FileField(label = soporte.nombre)

            if soporte_file != None:
                self.fields[str(soporte.id)].initial = soporte_file.archivo

            fields.append(Div(
                Div(str(soporte.id),css_class='col-sm-12'),
                css_class = 'row'
            ))


        self.helper.layout[0].fields = fields

class LegalizacionSeguridadForm(forms.Form):

    ids = forms.CharField(max_length=200,required=False,widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(LegalizacionSeguridadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        contrato = Contrato.objects.get(id = kwargs['initial']['id_contrato'])
        ids = contrato.soportes_requeridos.soportes_requeridos.filter(categoria = 'Seguridad Social').values_list('id',flat=True)
        self.fields['ids'].initial = unicode(ids)

        self.helper.layout = Layout(
            Fieldset(
                'Documentos de Seguridad Social',
            ),
            Div('ids'),
            HTML(
                """
                <p>*Cargue mensualmente la planilla PILA que soporte el pago de Seguridad Social, Pensión y Arl.</p>
                """
            )
        )

        fields = []

        for soporte in contrato.soportes_requeridos.soportes_requeridos.filter(categoria = 'Seguridad Social'):

            tipo = TipoSoporte.objects.get(id = soporte.id)

            soporte_file = None

            try:
                soporte_file = Soporte.objects.get(contrato = contrato,formador = contrato.formador,tipo = tipo)
            except:
                pass

            self.fields[str(soporte.id)] = forms.FileField(label = soporte.nombre,required=False)

            if soporte_file != None:
                self.fields[str(soporte.id)].initial = soporte_file.archivo

            fields.append(Div(
                Div(str(soporte.id),css_class='col-sm-12'),
                css_class = 'row'
            ))


        self.helper.layout[0].fields = fields