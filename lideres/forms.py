#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from administrativos.models import Administrativo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from lideres.models import Lideres, Soporte
from cargos.models import Cargo
from rh.models import TipoSoporte
from lideres.models import Contrato
from lideres.models import SolicitudSoportes

class LideresForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LideresForm, self).__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Usuario del sistema y Región',
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
            )
        )

    class Meta:
        model = Lideres
        fields = '__all__'
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ),
        }

class NuevoSoporteLiderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoSoporteLiderForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoSoporte.objects.exclude(oculto = True)
        if 'data' in kwargs:
            kwargs['data']['lider'] = kwargs['initial']['lider']
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

class LegalizacionLideresForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LegalizacionLideresForm, self).__init__(*args, **kwargs)
        dic = {
            'rut':6,
            'cedula':2,
            'policia':4,
            'procuraduria':5,
            'contraloria':11,
            'certificacion':9,
            'seguridad_social':8
        }


        soportes = Soporte.objects.filter(lider__cedula=kwargs['initial']['cedula'])

        rut = soportes.get(tipo__id=dic['rut'])
        fotocopia_cedula = soportes.get(tipo__id=dic['cedula'])
        antecedentes_judiciales = soportes.get(tipo__id=dic['policia'])
        antecedentes_procuraduria = soportes.get(tipo__id=dic['procuraduria'])
        antecedentes_contraloria = soportes.get(tipo__id=dic['contraloria'])
        certificacion = soportes.get(tipo__id=dic['certificacion'])
        seguridad_social = soportes.get(tipo__id=dic['seguridad_social'])

        self.helper = FormHelper(self)

        self.fields['rut'].initial = rut.archivo
        self.fields['fotocopia_cedula'].initial = fotocopia_cedula.archivo
        self.fields['antecedentes_judiciales'].initial = antecedentes_judiciales.archivo
        self.fields['antecedentes_procuraduria'].initial = antecedentes_procuraduria.archivo
        self.fields['antecedentes_contraloria'].initial = antecedentes_contraloria.archivo
        self.fields['certificacion'].initial = certificacion.archivo
        self.fields['seguridad_social'].initial = seguridad_social.archivo



        self.helper.layout = Layout(
            Div(
                Div(
                    Div('correo_personal',css_class='col-sm-4'),
                    Div('celular_personal',css_class='col-sm-4'),
                    Div('profesion',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('banco',css_class='col-sm-4'),
                    Div('tipo_cuenta',css_class='col-sm-4'),
                    Div('numero_cuenta',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('rut',css_class='col-sm-12 text-left'),

                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('fotocopia_cedula',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('antecedentes_judiciales',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('antecedentes_procuraduria',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('antecedentes_contraloria',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('certificacion',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                Div(
                    Div('seguridad_social',css_class='col-sm-12 text-left'),
                    css_class = 'row margin-bottom-row'
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
                    """),
                css_class='text-center'
            )
        )

    rut = forms.FileField(label="RUT")
    fotocopia_cedula = forms.FileField(label="Fotocopia de la cedula")
    antecedentes_judiciales = forms.FileField(label="Antecedentes judiciales (Policía)")
    antecedentes_procuraduria = forms.FileField(label="Antecedentes procuraduria")
    antecedentes_contraloria = forms.FileField(label="Antecedentes contraloría")
    certificacion = forms.FileField(label="Certificación bancaria")
    seguridad_social = forms.FileField(label="Seguridad social, ARL y Pensión de Agosto (opcional)",required=False)

    class Meta:
        model = Lideres
        fields = ['correo_personal','celular_personal','profesion','banco','tipo_cuenta','numero_cuenta']
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ,attrs={'required':'required'}),

            'correo_personal': forms.EmailInput(attrs={'required':'required'}),
            'celular_personal': forms.TextInput(attrs={'required':'required'}),
            'profesion': forms.TextInput(attrs={'required':'required'}),
            'banco': forms.Select(attrs={'required':'required'}),
            'numero_cuenta': forms.TextInput(attrs={'required':'required'}),
        }

        labels = {
            'correo_personal':'Email personal*',
            'celular_personal':'Numero de celular*',
            'profesion':'Profesión*',
            'banco':'Banco*',
            'tipo_cuenta':'Tipo cuenta*',
            'numero_cuenta':'Numero de cuenta*'
        }

class ConsultaLider(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConsultaLider, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('cedula',css_class='col-xs-12'),
                    css_class = 'row'
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Consultar</button></div>
                    """),
                css_class='text-center'
            )
        )

    def clean(self):
        cleaned_data = super(ConsultaLider, self).clean()
        cedula = cleaned_data.get('cedula')
        try:
            lider = Lideres.objects.get(cedula=cedula)
        except:
            self.add_error('cedula','No hay ningun lider registrado con este numero de cedula.')


    cedula = forms.IntegerField(label="Digita tu número de cedula (sin puntos o comas)")

class ContratoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)

        self.fields['lider'].initial = Lideres.objects.get(id = kwargs['initial']['id_lider'])

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
                    Div('lider',css_class='col-sm-6'),
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
        widgets = {'lider':forms.HiddenInput()}

class SolicitudSoportesLiderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitudSoportesLiderForm, self).__init__(*args, **kwargs)

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
                soporte_file = Soporte.objects.get(contrato = contrato,lider = contrato.lider,tipo = tipo)
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
                soporte_file = Soporte.objects.get(contrato = contrato,lider = contrato.lider,tipo = tipo)
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