#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from administrativos.models import Administrativo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from formadores.models import Formador
from cargos.models import Cargo
from rh.models import TipoSoporte
from formadores.models import Soporte
from django.forms.models import modelformset_factory
from formadores.models import Soporte
from departamentos.models import Departamento
from municipios.models import Municipio
from formadores.models import SolicitudTransporte
from formadores.models import Grupos
import locale
from formadores.models import Revision
from productos.models import Contratos, ValorEntregable
from formadores.models import Cortes, Contrato
from formadores.models import SolicitudSoportes
import datetime
from formadores.models import CohortesFormadores
from vigencia2017.models import TipoContrato

class FormadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormadorForm, self).__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.exclude(oculto = True)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Usuario del sistema',
                Div(
                    Div('usuario',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
            Fieldset(
                'Región',
                Div(
                    Div('region',css_class='col-sm-6'),
                    Div('usuario_colombia_aprende',css_class='col-sm-6'),
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
            Fieldset(
                'Lider',
                Div(
                    Div('lider',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Departamentos',
                Div(
                    Div('departamentos',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Ruta',
                Div(
                    Div('codigo_ruta',css_class='col-sm-6'),
                    Div('cantidad_docentes',css_class='col-sm-6'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = Formador
        fields = '__all__'
        widgets = {
            'tipo_cuenta': forms.Select(choices=(('','---------'),
                                                 ('Ahorros','Ahorros'),
                                                 ('Corriente','Corriente'),
                                                 )
                                        ),
        }

class ContratoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)

        self.fields['formador'].initial = Formador.objects.get(id = kwargs['initial']['id_formador'])
        self.fields['vigencia'].widget = forms.Select(choices=[('','---------'),('vigencia2017','Vigencia 2017')])

        choices = [('','----------')]

        for tipo in TipoContrato.objects.all():
            choices.append((tipo.id,tipo.nombre + " - " + tipo.get_valor_beneficiario()) )

        self.fields['tipo_contrato_id'].widget = forms.Select(choices=choices)

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
                    Div('formador',css_class='col-sm-6'),
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
            Fieldset(
                'Contrato original',
                Div(
                    Div('contrato_original',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Supervisión del contrato',
                Div(
                    Div('tipo_contrato_id', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('meta_beneficiarios', css_class='col-sm-4'),
                    Div('codigo_ruta', css_class='col-sm-4'),
                    Div('vigencia', css_class='col-sm-4'),
                    css_class='row'
                ),
                Div(
                    Div('supervisores',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('municipios',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = Contrato
        exclude = ['soportes']
        widgets = {'formador':forms.HiddenInput()}
        labels = {
            'fecha_inicio' : 'Fecha de inicio',
            'fecha_fin' : 'Fecha de finalización'
        }

class SolicitudSoportesFormadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitudSoportesFormadorForm, self).__init__(*args, **kwargs)

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

class NuevoSoporteFormadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoSoporteFormadorForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].queryset = TipoSoporte.objects.exclude(oculto = True)
        if 'data' in kwargs:
            kwargs['data']['formador'] = kwargs['initial']['formador']
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

class ConsultaFormador(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConsultaFormador, self).__init__(*args, **kwargs)
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
        cleaned_data = super(ConsultaFormador, self).clean()
        cedula = cleaned_data.get('cedula')
        try:
            formador = Formador.objects.get(cedula=cedula)
        except:
            self.add_error('cedula','No hay ningun formador registrado con este numero de cedula.')


    cedula = forms.IntegerField(label="Digita tu número de cedula (sin puntos o comas)")

'''
class LegalizacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LegalizacionForm, self).__init__(*args, **kwargs)
        dic = {
            'rut':6,
            'cedula':2,
            'policia':4,
            'procuraduria':5,
            'contraloria':11,
            'certificacion':9,
            'seguridad_social':8
        }


        soportes = Soporte.objects.filter(formador__cedula=kwargs['initial']['cedula'])

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
        model = Formador
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
'''

class NuevaSolicitudTransportes(forms.Form):
    nombre = forms.CharField(label="Nombre de la solicitud",max_length=20)

    fecha_1 = forms.DateField(label="Fecha")
    departamento_origen_1 = forms.CharField(label="Departamento (origen)",widget=forms.Select())
    municipio_origen_1 = forms.CharField(label="Municipio (origen)",widget=forms.Select())
    departamento_destino_1 = forms.CharField(label="Departamento (destino)",widget=forms.Select())
    municipio_destino_1 = forms.CharField(label="Municipio (destino)",widget=forms.Select())
    valor_1 = forms.CharField(label="Valor ($)")
    motivo_1 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),max_length=500)

    fecha_2 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_2 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_2 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_2 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_2 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_2 = forms.CharField(label="Valor ($)",required=False)
    motivo_2 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_3 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_3 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_3 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_3 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_3 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_3 = forms.CharField(label="Valor ($)",required=False)
    motivo_3 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_4 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_4 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_4 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_4 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_4 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_4 = forms.CharField(label="Valor ($)",required=False)
    motivo_4 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_5 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_5 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_5 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_5 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_5 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_5 = forms.CharField(label="Valor ($)",required=False)
    motivo_5 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_6 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_6 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_6 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_6 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_6 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_6 = forms.CharField(label="Valor ($)",required=False)
    motivo_6 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_7 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_7 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_7 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_7 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_7 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_7 = forms.CharField(label="Valor ($)",required=False)
    motivo_7 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_8 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_8 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_8 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_8 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_8 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_8 = forms.CharField(label="Valor ($)",required=False)
    motivo_8 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_9 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_9 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_9 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_9 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_9 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_9 = forms.CharField(label="Valor ($)",required=False)
    motivo_9 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    fecha_10 = forms.DateField(label="Nombre de la solicitud",required=False)
    departamento_origen_10 = forms.CharField(label="Departamento (origen)",widget=forms.Select(),required=False)
    municipio_origen_10 = forms.CharField(label="Municipio (origen)",widget=forms.Select(),required=False)
    departamento_destino_10 = forms.CharField(label="Departamento (destino)",widget=forms.Select(),required=False)
    municipio_destino_10 = forms.CharField(label="Municipio (destino)",widget=forms.Select(),required=False)
    valor_10 = forms.CharField(label="Valor ($)",required=False)
    motivo_10 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)

    def clean(self):
        cleaned_data = super(NuevaSolicitudTransportes, self).clean()

        fecha_2 = cleaned_data.get('fecha_2')
        departamento_origen_2 = cleaned_data.get('departamento_origen_2')
        municipio_origen_2 = cleaned_data.get('municipio_origen_2')
        departamento_destino_2 = cleaned_data.get('departamento_destino_2')
        municipio_destino_2 = cleaned_data.get('municipio_destino_2')
        valor_2 = cleaned_data.get('valor_2')
        motivo_2 = cleaned_data.get('motivo_2')

        fecha_3 = cleaned_data.get('fecha_3')
        departamento_origen_3 = cleaned_data.get('departamento_origen_3')
        municipio_origen_3 = cleaned_data.get('municipio_origen_3')
        departamento_destino_3 = cleaned_data.get('departamento_destino_3')
        municipio_destino_3 = cleaned_data.get('municipio_destino_3')
        valor_3 = cleaned_data.get('valor_3')
        motivo_3 = cleaned_data.get('motivo_3')

        fecha_4 = cleaned_data.get('fecha_4')
        departamento_origen_4 = cleaned_data.get('departamento_origen_4')
        municipio_origen_4 = cleaned_data.get('municipio_origen_4')
        departamento_destino_4 = cleaned_data.get('departamento_destino_4')
        municipio_destino_4 = cleaned_data.get('municipio_destino_4')
        valor_4 = cleaned_data.get('valor_4')
        motivo_4 = cleaned_data.get('motivo_4')

        fecha_5 = cleaned_data.get('fecha_5')
        departamento_origen_5 = cleaned_data.get('departamento_origen_5')
        municipio_origen_5 = cleaned_data.get('municipio_origen_5')
        departamento_destino_5 = cleaned_data.get('departamento_destino_5')
        municipio_destino_5 = cleaned_data.get('municipio_destino_5')
        valor_5 = cleaned_data.get('valor_5')
        motivo_5 = cleaned_data.get('motivo_5')

        fecha_6 = cleaned_data.get('fecha_6')
        departamento_origen_6 = cleaned_data.get('departamento_origen_6')
        municipio_origen_6 = cleaned_data.get('municipio_origen_6')
        departamento_destino_6 = cleaned_data.get('departamento_destino_6')
        municipio_destino_6 = cleaned_data.get('municipio_destino_6')
        valor_6 = cleaned_data.get('valor_6')
        motivo_6 = cleaned_data.get('motivo_6')

        fecha_7 = cleaned_data.get('fecha_7')
        departamento_origen_7 = cleaned_data.get('departamento_origen_7')
        municipio_origen_7 = cleaned_data.get('municipio_origen_7')
        departamento_destino_7 = cleaned_data.get('departamento_destino_7')
        municipio_destino_7 = cleaned_data.get('municipio_destino_7')
        valor_7 = cleaned_data.get('valor_7')
        motivo_7 = cleaned_data.get('motivo_7')

        fecha_8 = cleaned_data.get('fecha_8')
        departamento_origen_8 = cleaned_data.get('departamento_origen_8')
        municipio_origen_8 = cleaned_data.get('municipio_origen_8')
        departamento_destino_8 = cleaned_data.get('departamento_destino_8')
        municipio_destino_8 = cleaned_data.get('municipio_destino_8')
        valor_8 = cleaned_data.get('valor_8')
        motivo_8 = cleaned_data.get('motivo_8')

        fecha_9 = cleaned_data.get('fecha_9')
        departamento_origen_9 = cleaned_data.get('departamento_origen_9')
        municipio_origen_9 = cleaned_data.get('municipio_origen_9')
        departamento_destino_9 = cleaned_data.get('departamento_destino_9')
        municipio_destino_9 = cleaned_data.get('municipio_destino_9')
        valor_9 = cleaned_data.get('valor_9')
        motivo_9 = cleaned_data.get('motivo_9')

        fecha_10 = cleaned_data.get('fecha_10')
        departamento_origen_10 = cleaned_data.get('departamento_origen_10')
        municipio_origen_10 = cleaned_data.get('municipio_origen_10')
        departamento_destino_10 = cleaned_data.get('departamento_destino_10')
        municipio_destino_10 = cleaned_data.get('municipio_destino_10')
        valor_10 = cleaned_data.get('valor_10')
        motivo_10 = cleaned_data.get('motivo_10')

        if fecha_2 != None or departamento_origen_2 != "" or municipio_origen_2 != "" or departamento_destino_2 != "" or municipio_destino_2 != "" or valor_2 != "" or motivo_2 != "":

            if fecha_2 == None:
                self.add_error('fecha_2','Selecciona una fecha')

            if departamento_origen_2 == "":
                self.add_error('departamento_origen_2','Selecciona un departamento de origen')

            if municipio_origen_2 == "":
                self.add_error('municipio_origen_2','Selecciona un municipio de origen')

            if departamento_destino_2 == "":
                self.add_error('departamento_destino_2','Selecciona un departamento de destino')

            if municipio_destino_2 == "":
                self.add_error('municipio_destino_2','Selecciona un municipio de destino')

            if valor_2 == "":
                self.add_error('valor_2','Escribe un valor valido')

            if motivo_2 == "":
                self.add_error('motivo_2','Debes escribir el motivo del desplazamiento')


        if fecha_3 != None or departamento_origen_3 != "" or municipio_origen_3 != "" or departamento_destino_3 != "" or municipio_destino_3 != "" or valor_3 != "" or motivo_3 != "":

            if fecha_3 == None:
                self.add_error('fecha_3','Selecciona una fecha')

            if departamento_origen_3 == "":
                self.add_error('departamento_origen_3','Selecciona un departamento de origen')

            if municipio_origen_3 == "":
                self.add_error('municipio_origen_3','Selecciona un municipio de origen')

            if departamento_destino_3 == "":
                self.add_error('departamento_destino_3','Selecciona un departamento de destino')

            if municipio_destino_3 == "":
                self.add_error('municipio_destino_3','Selecciona un municipio de destino')

            if valor_3 == "":
                self.add_error('valor_3','Escribe un valor valido')

            if motivo_3 == "":
                self.add_error('motivo_3','Debes escribir el motivo del desplazamiento')


        if fecha_4 != None or departamento_origen_4 != "" or municipio_origen_4 != "" or departamento_destino_4 != "" or municipio_destino_4 != "" or valor_4 != "" or motivo_4 != "":

            if fecha_4 == None:
                self.add_error('fecha_4','Selecciona una fecha')

            if departamento_origen_4 == "":
                self.add_error('departamento_origen_4','Selecciona un departamento de origen')

            if municipio_origen_4 == "":
                self.add_error('municipio_origen_4','Selecciona un municipio de origen')

            if departamento_destino_4 == "":
                self.add_error('departamento_destino_4','Selecciona un departamento de destino')

            if municipio_destino_4 == "":
                self.add_error('municipio_destino_4','Selecciona un municipio de destino')

            if valor_4 == "":
                self.add_error('valor_4','Escribe un valor valido')

            if motivo_4 == "":
                self.add_error('motivo_4','Debes escribir el motivo del desplazamiento')


        if fecha_5 != None or departamento_origen_5 != "" or municipio_origen_5 != "" or departamento_destino_5 != "" or municipio_destino_5 != "" or valor_5 != "" or motivo_5 != "":

            if fecha_5 == None:
                self.add_error('fecha_5','Selecciona una fecha')

            if departamento_origen_5 == "":
                self.add_error('departamento_origen_5','Selecciona un departamento de origen')

            if municipio_origen_5 == "":
                self.add_error('municipio_origen_5','Selecciona un municipio de origen')

            if departamento_destino_5 == "":
                self.add_error('departamento_destino_5','Selecciona un departamento de destino')

            if municipio_destino_5 == "":
                self.add_error('municipio_destino_5','Selecciona un municipio de destino')

            if valor_5 == "":
                self.add_error('valor_5','Escribe un valor valido')

            if motivo_5 == "":
                self.add_error('motivo_5','Debes escribir el motivo del desplazamiento')


        if fecha_6 != None or departamento_origen_6 != "" or municipio_origen_6 != "" or departamento_destino_6 != "" or municipio_destino_6 != "" or valor_6 != "" or motivo_6 != "":

            if fecha_6 == None:
                self.add_error('fecha_6','Selecciona una fecha')

            if departamento_origen_6 == "":
                self.add_error('departamento_origen_6','Selecciona un departamento de origen')

            if municipio_origen_6 == "":
                self.add_error('municipio_origen_6','Selecciona un municipio de origen')

            if departamento_destino_6 == "":
                self.add_error('departamento_destino_6','Selecciona un departamento de destino')

            if municipio_destino_6 == "":
                self.add_error('municipio_destino_6','Selecciona un municipio de destino')

            if valor_6 == "":
                self.add_error('valor_6','Escribe un valor valido')

            if motivo_6 == "":
                self.add_error('motivo_6','Debes escribir el motivo del desplazamiento')


        if fecha_7 != None or departamento_origen_7 != "" or municipio_origen_7 != "" or departamento_destino_7 != "" or municipio_destino_7 != "" or valor_7 != "" or motivo_7 != "":

            if fecha_7 == None:
                self.add_error('fecha_7','Selecciona una fecha')

            if departamento_origen_7 == "":
                self.add_error('departamento_origen_7','Selecciona un departamento de origen')

            if municipio_origen_7 == "":
                self.add_error('municipio_origen_7','Selecciona un municipio de origen')

            if departamento_destino_7 == "":
                self.add_error('departamento_destino_7','Selecciona un departamento de destino')

            if municipio_destino_7 == "":
                self.add_error('municipio_destino_7','Selecciona un municipio de destino')

            if valor_7 == "":
                self.add_error('valor_7','Escribe un valor valido')

            if motivo_7 == "":
                self.add_error('motivo_7','Debes escribir el motivo del desplazamiento')

        if fecha_8 != None or departamento_origen_8 != "" or municipio_origen_8 != "" or departamento_destino_8 != "" or municipio_destino_8 != "" or valor_8 != "" or motivo_8 != "":

            if fecha_8 == None:
                self.add_error('fecha_8','Selecciona una fecha')

            if departamento_origen_8 == "":
                self.add_error('departamento_origen_8','Selecciona un departamento de origen')

            if municipio_origen_8 == "":
                self.add_error('municipio_origen_8','Selecciona un municipio de origen')

            if departamento_destino_8 == "":
                self.add_error('departamento_destino_8','Selecciona un departamento de destino')

            if municipio_destino_8 == "":
                self.add_error('municipio_destino_8','Selecciona un municipio de destino')

            if valor_8 == "":
                self.add_error('valor_8','Escribe un valor valido')

            if motivo_8 == "":
                self.add_error('motivo_8','Debes escribir el motivo del desplazamiento')

        if fecha_9 != None or departamento_origen_9 != "" or municipio_origen_9 != "" or departamento_destino_9 != "" or municipio_destino_9 != "" or valor_9 != "" or motivo_9 != "":

            if fecha_9 == None:
                self.add_error('fecha_9','Selecciona una fecha')

            if departamento_origen_9 == "":
                self.add_error('departamento_origen_9','Selecciona un departamento de origen')

            if municipio_origen_9 == "":
                self.add_error('municipio_origen_9','Selecciona un municipio de origen')

            if departamento_destino_9 == "":
                self.add_error('departamento_destino_9','Selecciona un departamento de destino')

            if municipio_destino_9 == "":
                self.add_error('municipio_destino_9','Selecciona un municipio de destino')

            if valor_9 == "":
                self.add_error('valor_9','Escribe un valor valido')

            if motivo_9 == "":
                self.add_error('motivo_9','Debes escribir el motivo del desplazamiento')


        if fecha_10 != None or departamento_origen_10 != "" or municipio_origen_10 != "" or departamento_destino_10 != "" or municipio_destino_10 != "" or valor_10 != "" or motivo_10 != "":

            if fecha_10 == None:
                self.add_error('fecha_10','Selecciona una fecha')

            if departamento_origen_10 == "":
                self.add_error('departamento_origen_10','Selecciona un departamento de origen')

            if municipio_origen_10 == "":
                self.add_error('municipio_origen_10','Selecciona un municipio de origen')

            if departamento_destino_10 == "":
                self.add_error('departamento_destino_10','Selecciona un departamento de destino')

            if municipio_destino_10 == "":
                self.add_error('municipio_destino_10','Selecciona un municipio de destino')

            if valor_10 == "":
                self.add_error('valor_10','Escribe un valor valido')

            if motivo_10 == "":
                self.add_error('motivo_10','Debes escribir el motivo del desplazamiento')


    def __init__(self, *args, **kwargs):
        super(NuevaSolicitudTransportes, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_origen_1'] != '':
                departamento_id = kwargs['data']['departamento_origen_1']
                self.fields['municipio_origen_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_2'] != '':
                departamento_id = kwargs['data']['departamento_origen_2']
                self.fields['municipio_origen_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_3'] != '':
                departamento_id = kwargs['data']['departamento_origen_3']
                self.fields['municipio_origen_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_4'] != '':
                departamento_id = kwargs['data']['departamento_origen_4']
                self.fields['municipio_origen_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_5'] != '':
                departamento_id = kwargs['data']['departamento_origen_5']
                self.fields['municipio_origen_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_6'] != '':
                departamento_id = kwargs['data']['departamento_origen_6']
                self.fields['municipio_origen_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_7'] != '':
                departamento_id = kwargs['data']['departamento_origen_7']
                self.fields['municipio_origen_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_8'] != '':
                departamento_id = kwargs['data']['departamento_origen_8']
                self.fields['municipio_origen_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_9'] != '':
                departamento_id = kwargs['data']['departamento_origen_9']
                self.fields['municipio_origen_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_10'] != '':
                departamento_id = kwargs['data']['departamento_origen_10']
                self.fields['municipio_origen_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')







            if kwargs['data']['departamento_destino_1'] != '':
                departamento_id = kwargs['data']['departamento_destino_1']
                self.fields['municipio_destino_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_2'] != '':
                departamento_id = kwargs['data']['departamento_destino_2']
                self.fields['municipio_destino_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_3'] != '':
                departamento_id = kwargs['data']['departamento_destino_3']
                self.fields['municipio_destino_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_4'] != '':
                departamento_id = kwargs['data']['departamento_destino_4']
                self.fields['municipio_destino_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_5'] != '':
                departamento_id = kwargs['data']['departamento_destino_5']
                self.fields['municipio_destino_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_6'] != '':
                departamento_id = kwargs['data']['departamento_destino_6']
                self.fields['municipio_destino_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_7'] != '':
                departamento_id = kwargs['data']['departamento_destino_7']
                self.fields['municipio_destino_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_8'] != '':
                departamento_id = kwargs['data']['departamento_destino_8']
                self.fields['municipio_destino_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_9'] != '':
                departamento_id = kwargs['data']['departamento_destino_9']
                self.fields['municipio_destino_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_10'] != '':
                departamento_id = kwargs['data']['departamento_destino_10']
                self.fields['municipio_destino_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

        departamentos_queryset = Departamento.objects.values_list('id','nombre')
        departamentos = [('','---------')]

        for y in departamentos_queryset:
            departamentos.append((str(y[0]),y[1]))


        self.fields['departamento_origen_1'].widget.choices = departamentos
        self.fields['departamento_origen_2'].widget.choices = departamentos
        self.fields['departamento_origen_3'].widget.choices = departamentos
        self.fields['departamento_origen_4'].widget.choices = departamentos
        self.fields['departamento_origen_5'].widget.choices = departamentos
        self.fields['departamento_origen_6'].widget.choices = departamentos
        self.fields['departamento_origen_7'].widget.choices = departamentos
        self.fields['departamento_origen_8'].widget.choices = departamentos
        self.fields['departamento_origen_9'].widget.choices = departamentos
        self.fields['departamento_origen_10'].widget.choices = departamentos


        self.fields['departamento_destino_1'].widget.choices = departamentos
        self.fields['departamento_destino_2'].widget.choices = departamentos
        self.fields['departamento_destino_3'].widget.choices = departamentos
        self.fields['departamento_destino_4'].widget.choices = departamentos
        self.fields['departamento_destino_5'].widget.choices = departamentos
        self.fields['departamento_destino_6'].widget.choices = departamentos
        self.fields['departamento_destino_7'].widget.choices = departamentos
        self.fields['departamento_destino_8'].widget.choices = departamentos
        self.fields['departamento_destino_9'].widget.choices = departamentos
        self.fields['departamento_destino_10'].widget.choices = departamentos


        self.helper.layout = Layout(
            Div(
                Div(
                    Div('nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Fieldset(
                    'Desplazamiento # 1',
                    Div(
                        Div('fecha_1',css_class='col-sm-2'),
                        Div('departamento_origen_1',css_class='col-sm-2'),
                        Div('municipio_origen_1',css_class='col-sm-2'),
                        Div('departamento_destino_1',css_class='col-sm-2'),
                        Div('municipio_destino_1',css_class='col-sm-2'),
                        Div('valor_1',css_class='col-sm-2'),
                        css_class = 'row'
                    ),

                    Div(
                        Div('motivo_1',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),
                Fieldset(
                    'Desplazamiento # 2',
                    Div(
                        Div('fecha_2',css_class='col-sm-2'),
                        Div('departamento_origen_2',css_class='col-sm-2'),
                        Div('municipio_origen_2',css_class='col-sm-2'),
                        Div('departamento_destino_2',css_class='col-sm-2'),
                        Div('municipio_destino_2',css_class='col-sm-2'),
                        Div('valor_2',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_2',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 3',
                    Div(
                        Div('fecha_3',css_class='col-sm-2'),
                        Div('departamento_origen_3',css_class='col-sm-2'),
                        Div('municipio_origen_3',css_class='col-sm-2'),
                        Div('departamento_destino_3',css_class='col-sm-2'),
                        Div('municipio_destino_3',css_class='col-sm-2'),
                        Div('valor_3',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_3',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 4',
                    Div(
                        Div('fecha_4',css_class='col-sm-2'),
                        Div('departamento_origen_4',css_class='col-sm-2'),
                        Div('municipio_origen_4',css_class='col-sm-2'),
                        Div('departamento_destino_4',css_class='col-sm-2'),
                        Div('municipio_destino_4',css_class='col-sm-2'),
                        Div('valor_4',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_4',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 5',
                    Div(
                        Div('fecha_5',css_class='col-sm-2'),
                        Div('departamento_origen_5',css_class='col-sm-2'),
                        Div('municipio_origen_5',css_class='col-sm-2'),
                        Div('departamento_destino_5',css_class='col-sm-2'),
                        Div('municipio_destino_5',css_class='col-sm-2'),
                        Div('valor_5',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_5',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 6',
                    Div(
                        Div('fecha_6',css_class='col-sm-2'),
                        Div('departamento_origen_6',css_class='col-sm-2'),
                        Div('municipio_origen_6',css_class='col-sm-2'),
                        Div('departamento_destino_6',css_class='col-sm-2'),
                        Div('municipio_destino_6',css_class='col-sm-2'),
                        Div('valor_6',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_6',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 7',
                    Div(
                        Div('fecha_7',css_class='col-sm-2'),
                        Div('departamento_origen_7',css_class='col-sm-2'),
                        Div('municipio_origen_7',css_class='col-sm-2'),
                        Div('departamento_destino_7',css_class='col-sm-2'),
                        Div('municipio_destino_7',css_class='col-sm-2'),
                        Div('valor_7',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_7',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 8',
                    Div(
                        Div('fecha_8',css_class='col-sm-2'),
                        Div('departamento_origen_8',css_class='col-sm-2'),
                        Div('municipio_origen_8',css_class='col-sm-2'),
                        Div('departamento_destino_8',css_class='col-sm-2'),
                        Div('municipio_destino_8',css_class='col-sm-2'),
                        Div('valor_8',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_8',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 9',
                    Div(
                        Div('fecha_9',css_class='col-sm-2'),
                        Div('departamento_origen_9',css_class='col-sm-2'),
                        Div('municipio_origen_9',css_class='col-sm-2'),
                        Div('departamento_destino_9',css_class='col-sm-2'),
                        Div('municipio_destino_9',css_class='col-sm-2'),
                        Div('valor_9',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_9',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                Fieldset(
                    'Desplazamiento # 10',
                    Div(
                        Div('fecha_10',css_class='col-sm-2'),
                        Div('departamento_origen_10',css_class='col-sm-2'),
                        Div('municipio_origen_10',css_class='col-sm-2'),
                        Div('departamento_destino_10',css_class='col-sm-2'),
                        Div('municipio_destino_10',css_class='col-sm-2'),
                        Div('valor_10',css_class='col-sm-2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_10',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
                    """),
                css_class='text-center'
            )
        )

class SolicitudTransporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Solicitud de transporte:',
                Div(
                    HTML("""
                    <p>Formador: {{object.formador.nombres}} {{object.formador.apellidos}}</p>
                    <p>Solicitud: {{object.nombre}}</p>
                    <p>Valor solicitado por el formador: {{valor_solicitado}}</p>
                    <p>Valor aprobado por el lider: {{valor_aprobado_lider}}</p>
                    <p>Archivo: <a href="{{archivo_url}}">{{archivo_nombre}}</a></p>
                    """)
                ),
                Div(
                    Div('estado',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('observacion',css_class='col-sm-12'),
                    css_class = 'row'
                )

            ),
        )

    class Meta:
        model = SolicitudTransporte
        fields = ['estado','observacion']
        widgets = {
            'estado' : forms.Select(choices=(('aprobado','Aprobado financiera'),('aprobado_lider','Aprobado lider'),('consignado','Consignado'),('revision','En revisión'),('rechazado','Rechazado')))
        }

class SubirSoporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubirSoporteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('archivo',css_class='col-sm-12 text-left'),
                css_class = 'row'
            ),

            HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
            """),

        )

    class Meta:
        model = SolicitudTransporte
        fields = ['archivo']

class SolicitudTransporteAdminForm(forms.Form):
    formador = forms.CharField(label="Formador",max_length=100,widget=forms.Select())
    nombre = forms.CharField(label="Nombre de la solicitud",max_length=20)

    fecha_1 = forms.DateField(label="Fecha")
    departamento_origen_1 = forms.CharField(label="Depto (origen)",widget=forms.Select())
    municipio_origen_1 = forms.CharField(label="Municipio (origen)",widget=forms.Select())
    departamento_destino_1 = forms.CharField(label="Depto (destino)",widget=forms.Select())
    municipio_destino_1 = forms.CharField(label="Municipio (destino)",widget=forms.Select())
    valor_1 = forms.CharField(label="Valor ($)")

    fecha_2 = forms.DateField(label="",required=False)
    departamento_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_2 = forms.CharField(label="",required=False)

    fecha_3 = forms.DateField(label="",required=False)
    departamento_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_3 = forms.CharField(label="",required=False)

    fecha_4 = forms.DateField(label="",required=False)
    departamento_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_4 = forms.CharField(label="",required=False)

    fecha_5 = forms.DateField(label="",required=False)
    departamento_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_5 = forms.CharField(label="",required=False)

    fecha_6 = forms.DateField(label="",required=False)
    departamento_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_6 = forms.CharField(label="",required=False)

    fecha_7 = forms.DateField(label="",required=False)
    departamento_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_7 = forms.CharField(label="",required=False)

    fecha_8 = forms.DateField(label="",required=False)
    departamento_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_8 = forms.CharField(label="",required=False)

    fecha_9 = forms.DateField(label="",required=False)
    departamento_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_9 = forms.CharField(label="",required=False)

    fecha_10 = forms.DateField(label="",required=False)
    departamento_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_10 = forms.CharField(label="",required=False)


    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_origen_1'] != '':
                departamento_id = kwargs['data']['departamento_origen_1']
                self.fields['municipio_origen_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_2'] != '':
                departamento_id = kwargs['data']['departamento_origen_2']
                self.fields['municipio_origen_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_3'] != '':
                departamento_id = kwargs['data']['departamento_origen_3']
                self.fields['municipio_origen_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_4'] != '':
                departamento_id = kwargs['data']['departamento_origen_4']
                self.fields['municipio_origen_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_origen_5'] != '':
                departamento_id = kwargs['data']['departamento_origen_5']
                self.fields['municipio_origen_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_6'] != '':
                departamento_id = kwargs['data']['departamento_origen_6']
                self.fields['municipio_origen_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_7'] != '':
                departamento_id = kwargs['data']['departamento_origen_7']
                self.fields['municipio_origen_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_8'] != '':
                departamento_id = kwargs['data']['departamento_origen_8']
                self.fields['municipio_origen_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_9'] != '':
                departamento_id = kwargs['data']['departamento_origen_9']
                self.fields['municipio_origen_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_origen_10'] != '':
                departamento_id = kwargs['data']['departamento_origen_10']
                self.fields['municipio_origen_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')







            if kwargs['data']['departamento_destino_1'] != '':
                departamento_id = kwargs['data']['departamento_destino_1']
                self.fields['municipio_destino_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_2'] != '':
                departamento_id = kwargs['data']['departamento_destino_2']
                self.fields['municipio_destino_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_3'] != '':
                departamento_id = kwargs['data']['departamento_destino_3']
                self.fields['municipio_destino_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_4'] != '':
                departamento_id = kwargs['data']['departamento_destino_4']
                self.fields['municipio_destino_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            if kwargs['data']['departamento_destino_5'] != '':
                departamento_id = kwargs['data']['departamento_destino_5']
                self.fields['municipio_destino_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_6'] != '':
                departamento_id = kwargs['data']['departamento_destino_6']
                self.fields['municipio_destino_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_7'] != '':
                departamento_id = kwargs['data']['departamento_destino_7']
                self.fields['municipio_destino_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_8'] != '':
                departamento_id = kwargs['data']['departamento_destino_8']
                self.fields['municipio_destino_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_9'] != '':
                departamento_id = kwargs['data']['departamento_destino_9']
                self.fields['municipio_destino_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')


            if kwargs['data']['departamento_destino_10'] != '':
                departamento_id = kwargs['data']['departamento_destino_10']
                self.fields['municipio_destino_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

        departamentos_queryset = Departamento.objects.values_list('id','nombre')
        departamentos = [('','---------')]

        for y in departamentos_queryset:
            departamentos.append((str(y[0]),y[1]))

        formadores_queryset = Formador.objects.all().values_list('id','nombres','apellidos')
        formadores = [('','---------')]

        for y in formadores_queryset:
            formadores.append((str(y[0]),y[1]+" "+y[2]))

        self.fields['formador'].widget.choices = formadores

        self.fields['departamento_origen_1'].widget.choices = departamentos
        self.fields['departamento_origen_2'].widget.choices = departamentos
        self.fields['departamento_origen_3'].widget.choices = departamentos
        self.fields['departamento_origen_4'].widget.choices = departamentos
        self.fields['departamento_origen_5'].widget.choices = departamentos
        self.fields['departamento_origen_6'].widget.choices = departamentos
        self.fields['departamento_origen_7'].widget.choices = departamentos
        self.fields['departamento_origen_8'].widget.choices = departamentos
        self.fields['departamento_origen_9'].widget.choices = departamentos
        self.fields['departamento_origen_10'].widget.choices = departamentos


        self.fields['departamento_destino_1'].widget.choices = departamentos
        self.fields['departamento_destino_2'].widget.choices = departamentos
        self.fields['departamento_destino_3'].widget.choices = departamentos
        self.fields['departamento_destino_4'].widget.choices = departamentos
        self.fields['departamento_destino_5'].widget.choices = departamentos
        self.fields['departamento_destino_6'].widget.choices = departamentos
        self.fields['departamento_destino_7'].widget.choices = departamentos
        self.fields['departamento_destino_8'].widget.choices = departamentos
        self.fields['departamento_destino_9'].widget.choices = departamentos
        self.fields['departamento_destino_10'].widget.choices = departamentos


        self.helper.layout = Layout(
            Div(
                Div(
                    Div('formador',css_class='col-sm-6'),
                    Div('nombre',css_class='col-sm-6'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_1',css_class='col-sm-2'),
                    Div('departamento_origen_1',css_class='col-sm-2'),
                    Div('municipio_origen_1',css_class='col-sm-2'),
                    Div('departamento_destino_1',css_class='col-sm-2'),
                    Div('municipio_destino_1',css_class='col-sm-2'),
                    Div('valor_1',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_2',css_class='col-sm-2'),
                    Div('departamento_origen_2',css_class='col-sm-2'),
                    Div('municipio_origen_2',css_class='col-sm-2'),
                    Div('departamento_destino_2',css_class='col-sm-2'),
                    Div('municipio_destino_2',css_class='col-sm-2'),
                    Div('valor_2',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_3',css_class='col-sm-2'),
                    Div('departamento_origen_3',css_class='col-sm-2'),
                    Div('municipio_origen_3',css_class='col-sm-2'),
                    Div('departamento_destino_3',css_class='col-sm-2'),
                    Div('municipio_destino_3',css_class='col-sm-2'),
                    Div('valor_3',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_4',css_class='col-sm-2'),
                    Div('departamento_origen_4',css_class='col-sm-2'),
                    Div('municipio_origen_4',css_class='col-sm-2'),
                    Div('departamento_destino_4',css_class='col-sm-2'),
                    Div('municipio_destino_4',css_class='col-sm-2'),
                    Div('valor_4',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_5',css_class='col-sm-2'),
                    Div('departamento_origen_5',css_class='col-sm-2'),
                    Div('municipio_origen_5',css_class='col-sm-2'),
                    Div('departamento_destino_5',css_class='col-sm-2'),
                    Div('municipio_destino_5',css_class='col-sm-2'),
                    Div('valor_5',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_6',css_class='col-sm-2'),
                    Div('departamento_origen_6',css_class='col-sm-2'),
                    Div('municipio_origen_6',css_class='col-sm-2'),
                    Div('departamento_destino_6',css_class='col-sm-2'),
                    Div('municipio_destino_6',css_class='col-sm-2'),
                    Div('valor_6',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_7',css_class='col-sm-2'),
                    Div('departamento_origen_7',css_class='col-sm-2'),
                    Div('municipio_origen_7',css_class='col-sm-2'),
                    Div('departamento_destino_7',css_class='col-sm-2'),
                    Div('municipio_destino_7',css_class='col-sm-2'),
                    Div('valor_7',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_8',css_class='col-sm-2'),
                    Div('departamento_origen_8',css_class='col-sm-2'),
                    Div('municipio_origen_8',css_class='col-sm-2'),
                    Div('departamento_destino_8',css_class='col-sm-2'),
                    Div('municipio_destino_8',css_class='col-sm-2'),
                    Div('valor_8',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_9',css_class='col-sm-2'),
                    Div('departamento_origen_9',css_class='col-sm-2'),
                    Div('municipio_origen_9',css_class='col-sm-2'),
                    Div('departamento_destino_9',css_class='col-sm-2'),
                    Div('municipio_destino_9',css_class='col-sm-2'),
                    Div('valor_9',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('fecha_10',css_class='col-sm-2'),
                    Div('departamento_origen_10',css_class='col-sm-2'),
                    Div('municipio_origen_10',css_class='col-sm-2'),
                    Div('departamento_destino_10',css_class='col-sm-2'),
                    Div('municipio_destino_10',css_class='col-sm-2'),
                    Div('valor_10',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                css_class='text-center'
            )
        )

class SolicitudTransporteUpdateForm(forms.Form):
    formador = forms.CharField(label="Formador",max_length=100,widget=forms.Select())
    nombre = forms.CharField(label="Nombre de la solicitud",max_length=20)

    fecha_1 = forms.DateField(label="Fecha")
    departamento_origen_1 = forms.CharField(label="Depto (origen)",widget=forms.Select())
    municipio_origen_1 = forms.CharField(label="Municipio (origen)",widget=forms.Select())
    departamento_destino_1 = forms.CharField(label="Depto (destino)",widget=forms.Select())
    municipio_destino_1 = forms.CharField(label="Municipio (destino)",widget=forms.Select())
    valor_1 = forms.CharField(label="Valor ($)")
    motivo_1 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),max_length=500)
    id_1 = forms.CharField(max_length=100,widget=forms.HiddenInput())

    fecha_2 = forms.DateField(label="",required=False)
    departamento_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_2 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_2 = forms.CharField(label="",required=False)
    motivo_2 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_2 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_3 = forms.DateField(label="",required=False)
    departamento_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_3 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_3 = forms.CharField(label="",required=False)
    motivo_3 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_3 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_4 = forms.DateField(label="",required=False)
    departamento_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_4 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_4 = forms.CharField(label="",required=False)
    motivo_4 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_4 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_5 = forms.DateField(label="",required=False)
    departamento_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_5 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_5 = forms.CharField(label="",required=False)
    motivo_5 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_5 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_6 = forms.DateField(label="",required=False)
    departamento_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_6 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_6 = forms.CharField(label="",required=False)
    motivo_6 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_6 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_7 = forms.DateField(label="",required=False)
    departamento_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_7 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_7 = forms.CharField(label="",required=False)
    motivo_7 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_7 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_8 = forms.DateField(label="",required=False)
    departamento_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_8 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_8 = forms.CharField(label="",required=False)
    motivo_8 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_8 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_9 = forms.DateField(label="",required=False)
    departamento_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_9 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_9 = forms.CharField(label="",required=False)
    motivo_9 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_9 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fecha_10 = forms.DateField(label="",required=False)
    departamento_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_origen_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    departamento_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    municipio_destino_10 = forms.CharField(label="",widget=forms.Select(),required=False)
    valor_10 = forms.CharField(label="",required=False)
    motivo_10 = forms.CharField(label="Motivo desplazamiento",widget=forms.Textarea(attrs={'rows':5}),required=False,max_length=500)
    id_10 = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)


    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_origen_1'] != '':
                departamento_id = kwargs['data']['departamento_origen_1']
                self.fields['municipio_origen_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')

            try:
                if kwargs['data']['departamento_origen_2'] != '':
                    departamento_id = kwargs['data']['departamento_origen_2']
                    self.fields['municipio_origen_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_3'] != '':
                    departamento_id = kwargs['data']['departamento_origen_3']
                    self.fields['municipio_origen_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_4'] != '':
                    departamento_id = kwargs['data']['departamento_origen_4']
                    self.fields['municipio_origen_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_5'] != '':
                    departamento_id = kwargs['data']['departamento_origen_5']
                    self.fields['municipio_origen_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_6'] != '':
                    departamento_id = kwargs['data']['departamento_origen_6']
                    self.fields['municipio_origen_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_7'] != '':
                    departamento_id = kwargs['data']['departamento_origen_7']
                    self.fields['municipio_origen_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_8'] != '':
                    departamento_id = kwargs['data']['departamento_origen_8']
                    self.fields['municipio_origen_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_9'] != '':
                    departamento_id = kwargs['data']['departamento_origen_9']
                    self.fields['municipio_origen_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass

            try:
                if kwargs['data']['departamento_origen_10'] != '':
                    departamento_id = kwargs['data']['departamento_origen_10']
                    self.fields['municipio_origen_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass





            try:
                if kwargs['data']['departamento_destino_1'] != '':
                    departamento_id = kwargs['data']['departamento_destino_1']
                    self.fields['municipio_destino_1'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_2'] != '':
                    departamento_id = kwargs['data']['departamento_destino_2']
                    self.fields['municipio_destino_2'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_3'] != '':
                    departamento_id = kwargs['data']['departamento_destino_3']
                    self.fields['municipio_destino_3'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_4'] != '':
                    departamento_id = kwargs['data']['departamento_destino_4']
                    self.fields['municipio_destino_4'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_5'] != '':
                    departamento_id = kwargs['data']['departamento_destino_5']
                    self.fields['municipio_destino_5'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_6'] != '':
                    departamento_id = kwargs['data']['departamento_destino_6']
                    self.fields['municipio_destino_6'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_7'] != '':
                    departamento_id = kwargs['data']['departamento_destino_7']
                    self.fields['municipio_destino_7'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_8'] != '':
                    departamento_id = kwargs['data']['departamento_destino_8']
                    self.fields['municipio_destino_8'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_9'] != '':
                    departamento_id = kwargs['data']['departamento_destino_9']
                    self.fields['municipio_destino_9'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
            try:
                if kwargs['data']['departamento_destino_10'] != '':
                    departamento_id = kwargs['data']['departamento_destino_10']
                    self.fields['municipio_destino_10'].widget.choices = Municipio.objects.filter(departamento__id=departamento_id).values_list('id','nombre')
            except:
                pass
        departamentos_queryset = Departamento.objects.values_list('id','nombre')
        departamentos = [('','---------')]

        for y in departamentos_queryset:
            departamentos.append((str(y[0]),y[1]))

        formadores_queryset = Formador.objects.all().values_list('id','nombres','apellidos')
        formadores = [('','---------')]

        for y in formadores_queryset:
            formadores.append((str(y[0]),y[1]+" "+y[2]))

        self.fields['formador'].widget.choices = formadores

        self.fields['departamento_origen_1'].widget.choices = departamentos
        self.fields['departamento_origen_2'].widget.choices = departamentos
        self.fields['departamento_origen_3'].widget.choices = departamentos
        self.fields['departamento_origen_4'].widget.choices = departamentos
        self.fields['departamento_origen_5'].widget.choices = departamentos
        self.fields['departamento_origen_6'].widget.choices = departamentos
        self.fields['departamento_origen_7'].widget.choices = departamentos
        self.fields['departamento_origen_8'].widget.choices = departamentos
        self.fields['departamento_origen_9'].widget.choices = departamentos
        self.fields['departamento_origen_10'].widget.choices = departamentos


        self.fields['departamento_destino_1'].widget.choices = departamentos
        self.fields['departamento_destino_2'].widget.choices = departamentos
        self.fields['departamento_destino_3'].widget.choices = departamentos
        self.fields['departamento_destino_4'].widget.choices = departamentos
        self.fields['departamento_destino_5'].widget.choices = departamentos
        self.fields['departamento_destino_6'].widget.choices = departamentos
        self.fields['departamento_destino_7'].widget.choices = departamentos
        self.fields['departamento_destino_8'].widget.choices = departamentos
        self.fields['departamento_destino_9'].widget.choices = departamentos
        self.fields['departamento_destino_10'].widget.choices = departamentos

        solicitud = SolicitudTransporte.objects.get(id=kwargs['initial']['pk'])
        desplazamientos = solicitud.desplazamientos.all()

        i = 0

        self.fields['formador'].initial = solicitud.formador.id
        self.fields['nombre'].initial = solicitud.nombre

        for desplazamiento in desplazamientos:
            i += 1
            self.fields['id_'+str(i)].initial = desplazamiento.id
            self.fields['fecha_'+str(i)].initial = desplazamiento.fecha
            self.fields['departamento_origen_'+str(i)].initial = desplazamiento.departamento_origen.id
            self.fields['municipio_origen_'+str(i)].widget.choices = Municipio.objects.filter(departamento__id=desplazamiento.departamento_origen.id).values_list('id','nombre')
            self.fields['municipio_origen_'+str(i)].initial = desplazamiento.municipio_origen.id
            self.fields['departamento_destino_'+str(i)].initial = desplazamiento.departamento_destino.id
            self.fields['municipio_destino_'+str(i)].widget.choices = Municipio.objects.filter(departamento__id=desplazamiento.departamento_destino.id).values_list('id','nombre')
            self.fields['municipio_destino_'+str(i)].initial = desplazamiento.municipio_destino.id
            self.fields['valor_'+str(i)].initial = "{:,}".format(float(str(round(desplazamiento.valor)))) + '0'
            self.fields['motivo_'+str(i)].initial = desplazamiento.motivo

        for y in range(i,10):
            i += 1
            self.fields['id_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['fecha_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['departamento_origen_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_origen_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_origen_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['departamento_destino_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_destino_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['municipio_destino_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['valor_'+str(i)].widget.attrs['disabled'] = 'disabled'
            self.fields['motivo_'+str(i)].widget.attrs['disabled'] = 'disabled'


        self.helper.layout = Layout(
            Div(
                Div(
                    Div('formador',css_class='col-sm-6'),
                    Div('nombre',css_class='col-sm-6'),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 1',
                    Div(
                        Div('fecha_1',css_class='col-sm-2'),
                        Div('departamento_origen_1',css_class='col-sm-2'),
                        Div('municipio_origen_1',css_class='col-sm-2'),
                        Div('departamento_destino_1',css_class='col-sm-2'),
                        Div('municipio_destino_1',css_class='col-sm-2'),
                        Div('valor_1',css_class='col-sm-2'),
                        Div('id_1'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_1',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 2',
                    Div(
                        Div('fecha_2',css_class='col-sm-2'),
                        Div('departamento_origen_2',css_class='col-sm-2'),
                        Div('municipio_origen_2',css_class='col-sm-2'),
                        Div('departamento_destino_2',css_class='col-sm-2'),
                        Div('municipio_destino_2',css_class='col-sm-2'),
                        Div('valor_2',css_class='col-sm-2'),
                        Div('id_2'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_2',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 3',
                    Div(
                        Div('fecha_3',css_class='col-sm-2'),
                        Div('departamento_origen_3',css_class='col-sm-2'),
                        Div('municipio_origen_3',css_class='col-sm-2'),
                        Div('departamento_destino_3',css_class='col-sm-2'),
                        Div('municipio_destino_3',css_class='col-sm-2'),
                        Div('valor_3',css_class='col-sm-2'),
                        Div('id_3'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_3',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 4',
                    Div(
                        Div('fecha_4',css_class='col-sm-2'),
                        Div('departamento_origen_4',css_class='col-sm-2'),
                        Div('municipio_origen_4',css_class='col-sm-2'),
                        Div('departamento_destino_4',css_class='col-sm-2'),
                        Div('municipio_destino_4',css_class='col-sm-2'),
                        Div('valor_4',css_class='col-sm-2'),
                        Div('id_4'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_4',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 5',
                    Div(
                        Div('fecha_5',css_class='col-sm-2'),
                        Div('departamento_origen_5',css_class='col-sm-2'),
                        Div('municipio_origen_5',css_class='col-sm-2'),
                        Div('departamento_destino_5',css_class='col-sm-2'),
                        Div('municipio_destino_5',css_class='col-sm-2'),
                        Div('valor_5',css_class='col-sm-2'),
                        Div('id_5'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_5',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 6',
                    Div(
                        Div('fecha_6',css_class='col-sm-2'),
                        Div('departamento_origen_6',css_class='col-sm-2'),
                        Div('municipio_origen_6',css_class='col-sm-2'),
                        Div('departamento_destino_6',css_class='col-sm-2'),
                        Div('municipio_destino_6',css_class='col-sm-2'),
                        Div('valor_6',css_class='col-sm-2'),
                        Div('id_6'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_6',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 7',
                    Div(
                        Div('fecha_7',css_class='col-sm-2'),
                        Div('departamento_origen_7',css_class='col-sm-2'),
                        Div('municipio_origen_7',css_class='col-sm-2'),
                        Div('departamento_destino_7',css_class='col-sm-2'),
                        Div('municipio_destino_7',css_class='col-sm-2'),
                        Div('valor_7',css_class='col-sm-2'),
                        Div('id_7'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_7',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 8',
                    Div(
                        Div('fecha_8',css_class='col-sm-2'),
                        Div('departamento_origen_8',css_class='col-sm-2'),
                        Div('municipio_origen_8',css_class='col-sm-2'),
                        Div('departamento_destino_8',css_class='col-sm-2'),
                        Div('municipio_destino_8',css_class='col-sm-2'),
                        Div('valor_8',css_class='col-sm-2'),
                        Div('id_8'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_8',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),
                Fieldset(
                    'Desplazamiento # 9',
                    Div(
                        Div('fecha_9',css_class='col-sm-2'),
                        Div('departamento_origen_9',css_class='col-sm-2'),
                        Div('municipio_origen_9',css_class='col-sm-2'),
                        Div('departamento_destino_9',css_class='col-sm-2'),
                        Div('municipio_destino_9',css_class='col-sm-2'),
                        Div('valor_9',css_class='col-sm-2'),
                        Div('id_9'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_9',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                Fieldset(
                    'Desplazamiento # 10',
                    Div(
                        Div('fecha_10',css_class='col-sm-2'),
                        Div('departamento_origen_10',css_class='col-sm-2'),
                        Div('municipio_origen_10',css_class='col-sm-2'),
                        Div('departamento_destino_10',css_class='col-sm-2'),
                        Div('municipio_destino_10',css_class='col-sm-2'),
                        Div('valor_10',css_class='col-sm-2'),
                        Div('id_10'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('motivo_10',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class = 'row'
                ),

                css_class='text-center'
            )
        )

class SolicitudTransporteLiderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitudTransporteLiderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['aprobacion_lider'].initial = datetime.datetime.now()
        self.helper.layout = Layout(
            Fieldset(
                'Solicitud de transporte:',
                Div(
                    HTML("""
                    <p>Formador: {{object.formador.nombres}} {{object.formador.apellidos}}</p>
                    <p>Solicitud: {{object.nombre}}</p>
                    <p>Valor solicitado: {{valor}}</p>
                    <p>Archivo: <a href="{{object.get_archivo_url}}">{{object.archivo_filename}}</a></p>
                    """)
                ),
                Div(
                    Div('estado',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('observacion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('aprobacion_lider',css_class='col-sm-12'),
                    css_class = 'hidden'
                )
            ),
        )

    class Meta:
        model = SolicitudTransporte
        fields = ['estado','observacion','aprobacion_lider']
        widgets = {
            'estado' : forms.Select(choices=(('aprobado_lider','Aprobado'),('revision','En revisión'),('rechazado','Rechazado'))),
        }

class OtroSiForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OtroSiForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div('archivo',css_class='col-sm-12'),
                css_class = 'row'
            ),
            Div(
                Div('observacion',css_class='col-sm-12'),
                css_class = 'row'
            ),
            HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
                    """),
        )

    class Meta:
        model = Soporte
        fields = ['archivo']

class SeguridadSocialForm(forms.Form):

    agosto = forms.FileField(label="Agosto:",required=False)
    septiembre = forms.FileField(label="Septiembre:",required=False)
    octubre = forms.FileField(label="Octubre:",required=False)
    noviembre = forms.FileField(label="Noviembre:",required=False)
    diciembre = forms.FileField(label="Diciembre:",required=False)

    def __init__(self, *args, **kwargs):
        super(SeguridadSocialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        formador = Formador.objects.get(cedula=kwargs['initial']['cedula'])

        self.fields['agosto'].initial = Soporte.objects.filter(formador = formador).get(tipo__id = 8).archivo
        self.fields['septiembre'].initial = Soporte.objects.filter(formador = formador).get(tipo__id = 17).archivo
        self.fields['octubre'].initial = Soporte.objects.filter(formador = formador).get(tipo__id = 18).archivo
        self.fields['noviembre'].initial = Soporte.objects.filter(formador = formador).get(tipo__id = 19).archivo
        self.fields['diciembre'].initial = Soporte.objects.filter(formador = formador).get(tipo__id = 20).archivo

        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Seguridad social de agosto:',
                    Div(
                        Div('agosto',css_class='col-xs-12'),
                        css_class = 'row'
                    ),
                ),
                Fieldset(
                    'Seguridad social de septiembre:',
                    Div(
                        Div('septiembre',css_class='col-xs-12'),
                        css_class = 'row'
                    ),
                ),
                Fieldset(
                    'Seguridad social de octubre:',
                    Div(
                        Div('octubre',css_class='col-xs-12'),
                        css_class = 'row'
                    ),
                ),
                Fieldset(
                    'Seguridad social de noviembre:',
                    Div(
                        Div('noviembre',css_class='col-xs-12'),
                        css_class = 'row'
                    ),
                ),
                Fieldset(
                    'Seguridad social de diciembre:',
                    Div(
                        Div('diciembre',css_class='col-xs-12'),
                        css_class = 'row'
                    ),
                ),

                HTML("""
                    <div class="row"><button type="submit" class="btn btn-cpe">Enviar</button></div>
                    """),
            )
        )

class GruposForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(GruposForm, self).clean()
        nombre = cleaned_data.get('nombre')
        formador = cleaned_data.get('formador')

        if Grupos.objects.filter(formador = formador,nombre=nombre,oculto=False).count() > 0:
            self.add_error('nombre','Hay un grupo con el mismo nombre')




    def __init__(self, *args, **kwargs):
        super(GruposForm, self).__init__(*args, **kwargs)
        self.fields['formador'].initial = Formador.objects.get(id = kwargs['initial']['formador_id'])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Nombre',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('formador',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
            )
        )

    class Meta:
        model = Grupos
        fields = '__all__'
        widgets = {
            'nombre': forms.NumberInput(),
        }

class RevisionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RevisionForm, self).__init__(*args, **kwargs)

        formador = Formador.objects.get(id = kwargs['initial']['formador_id'])
        self.fields['formador_revision'].initial = formador

        cargo = Cargo.objects.get(id = kwargs['initial']['cargo_id'])

        contrato = Contratos.objects.filter(cargo = cargo).get(nombre = 'Capacitación 1') if formador.primera_capacitacion else Contratos.objects.filter(cargo = cargo).get(nombre = 'Capacitación 2')
        entregables = ValorEntregable.objects.filter(contrato = contrato)
        revisiones = Revision.objects.filter(formador_revision = formador)

        maximos = {}

        for revision in revisiones:
            for producto in revision.productos.all():
                id = producto.valor_entregable.entregable.id
                if 'field_' + str(id) in maximos.keys():
                    maximos['field_' + str(id)] += producto.cantidad
                else:
                    maximos['field_' + str(id)] = producto.cantidad


        self.helper = FormHelper(self)

        dict = {
            'Nivel 0':{
                'Presencial':[],
                'Virtual':[]
            },
            'Nivel 1':{
                'Presencial':[],
                'Virtual':[]
            },
            'Nivel 2':{
                'Presencial':[],
                'Virtual':[]
            },
            'Nivel 3':{
                'Presencial':[],
                'Virtual':[]
            },
            'Socializacion':{
                'Presencial':[],
                'Virtual':[]
            },
        }



        for entregable in entregables:
            field = 'field_' + str(entregable.entregable.id)
            self.fields[field] = forms.IntegerField()
            self.fields[field].required = False
            self.fields[field].initial = 0
            if field not in maximos.keys():
                max = 0
            else:
                max = maximos[field]

            self.fields[field].label = 'Max: ' + str(formador.cantidad_docentes - max) + ' - Pago: '+ str(max) +' - ' + entregable.entregable.tipo + ' - ' + entregable.entregable.sesion.nombre + ' - ' + entregable.entregable.nombre

            if entregable.entregable.sesion.nivel.nombre == "Nivel 0":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 0']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 0']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Nivel 1":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 1']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 1']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Nivel 2":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 2']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 2']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Nivel 3":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 3']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 3']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Socializacion":
                if entregable.entregable.tipo == "Presencial":
                    dict['Socializacion']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Socializacion']['Virtual'].append('field_' + str(entregable.entregable.id))


        for nivel in ['Nivel 0','Nivel 1','Nivel 2','Nivel 3','Socializacion']:
            if len(dict[nivel]['Presencial']) > 0 or len(dict[nivel]['Virtual']) > 0:
                self.helper.layout.fields.append(
                    Fieldset(
                        nivel,
                        css_id = nivel
                    )
                )

                self.helper.layout.fields[-1].fields = dict[nivel]['Presencial'] + dict[nivel]['Virtual']


        self.fields['formador_revision'].widget = forms.HiddenInput()

    def clean(self):

        cargo = Cargo.objects.get(id = self.initial['cargo_id'])

        cleaned_data = super(RevisionForm, self).clean()
        formador = cleaned_data.get('formador_revision')

        contrato = Contratos.objects.filter(cargo = cargo).get(nombre = 'Capacitación 1') if formador.primera_capacitacion else Contratos.objects.filter(cargo = cargo).get(nombre = 'Capacitación 2')
        entregables = ValorEntregable.objects.filter(contrato = contrato)
        revisiones = Revision.objects.filter(formador_revision = formador)

        maximos = {}

        for revision in revisiones:
            for producto in revision.productos.all():
                id = producto.valor_entregable.entregable.id
                if 'field_' + str(id) in maximos.keys():
                    maximos['field_' + str(id)] += producto.cantidad
                else:
                    maximos['field_' + str(id)] = producto.cantidad


        for entregable in entregables:
            field = 'field_' + str(entregable.entregable.id)
            if field not in maximos.keys():
                max = 0
            else:
                max = maximos[field]
            if formador.cantidad_docentes - max - cleaned_data.get(field) < 0:
                self.add_error(field,'En este producto se pueden añadir hasta ' + str(formador.cantidad_docentes - max) + ' beneficiarios.')


    class Meta:
        model = Revision
        fields = ['formador_revision','descripcion']

class RevisionUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RevisionUpdateForm, self).__init__(*args, **kwargs)

        revision_object = Revision.objects.get(id = kwargs['initial']['id'])
        formador = revision_object.formador_revision

        revisiones = Revision.objects.filter(formador_revision = formador).exclude(id = revision_object.id)

        maximos = {}

        for revision in revisiones:
            for producto in revision.productos.all():
                id = producto.valor_entregable.entregable.id
                if 'field_' + str(id) in maximos.keys():
                    maximos['field_' + str(id)] += producto.cantidad
                else:
                    maximos['field_' + str(id)] = producto.cantidad


        self.helper = FormHelper(self)

        dict = {
            'Nivel 0':{
                'Presencial':[],
                'Virtual':[]
            },
            'Nivel 1':{
                'Presencial':[],
                'Virtual':[]
            },
            'Nivel 2':{
                'Presencial':[],
                'Virtual':[]
            },
            'Nivel 3':{
                'Presencial':[],
                'Virtual':[]
            },
            'Socializacion':{
                'Presencial':[],
                'Virtual':[]
            },
        }



        for producto in revision_object.productos.all():
            entregable = producto.valor_entregable
            field = 'field_' + str(entregable.entregable.id)
            self.fields[field] = forms.IntegerField()
            self.fields[field].required = False
            self.fields[field].initial = producto.cantidad
            if field not in maximos.keys():
                max = 0
            else:
                max = maximos[field]

            self.fields[field].label = 'Max: ' + str(formador.cantidad_docentes - max) + ' - ' + entregable.entregable.tipo + ' - ' + entregable.entregable.sesion.nombre + ' - ' + entregable.entregable.nombre

            if entregable.entregable.sesion.nivel.nombre == "Nivel 0":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 0']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 0']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Nivel 1":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 1']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 1']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Nivel 2":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 2']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 2']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Nivel 3":
                if entregable.entregable.tipo == "Presencial":
                    dict['Nivel 3']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Nivel 3']['Virtual'].append('field_' + str(entregable.entregable.id))

            elif entregable.entregable.sesion.nivel.nombre == "Socializacion":
                if entregable.entregable.tipo == "Presencial":
                    dict['Socializacion']['Presencial'].append('field_' + str(entregable.entregable.id))
                if entregable.entregable.tipo == "Virtual":
                    dict['Socializacion']['Virtual'].append('field_' + str(entregable.entregable.id))


        for nivel in ['Nivel 0','Nivel 1','Nivel 2','Nivel 3','Socializacion']:
            if len(dict[nivel]['Presencial']) > 0 or len(dict[nivel]['Virtual']) > 0:
                self.helper.layout.fields.append(
                    Fieldset(
                        nivel,
                        css_id = nivel
                    )
                )

                self.helper.layout.fields[-1].fields = dict[nivel]['Presencial'] + dict[nivel]['Virtual']


        self.fields['formador_revision'].widget = forms.HiddenInput()

    def clean(self,**kwargs):
        cleaned_data = super(RevisionUpdateForm, self).clean()

        revision_object = Revision.objects.get(id = self.initial['id'])
        formador = revision_object.formador_revision

        revisiones = Revision.objects.filter(formador_revision = formador).exclude(id=revision_object.id)

        maximos = {}

        for revision in revisiones:
            for producto in revision.productos.all():
                id = producto.valor_entregable.entregable.id
                if 'field_' + str(id) in maximos.keys():
                    maximos['field_' + str(id)] += producto.cantidad
                else:
                    maximos['field_' + str(id)] = producto.cantidad


        for producto in revision_object.productos.all():
            entregable = producto.valor_entregable
            field = 'field_' + str(entregable.entregable.id)
            if field not in maximos.keys():
                max = 0
            else:
                max = maximos[field]
            if formador.cantidad_docentes - max - cleaned_data.get(field) < 0:
                self.add_error(field,'En este producto se pueden añadir hasta ' + str(formador.cantidad_docentes - max) + ' beneficiarios.')


    class Meta:
        model = Revision
        fields = ['formador_revision','descripcion']

class CortesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(CortesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['fecha'] = forms.CharField(max_length=100)

        self.helper.layout = Layout(
            Fieldset(
                'Corte de pago',
                Div(
                    Div('fecha',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                HTML(
                    """
                    <h4>Se va a hacer el corte para {{cantidad}} formador(es).</h4>
                    """
                ),
            )
        )

    class Meta:
        model = Cortes
        fields = ['descripcion']

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
                soporte_file = Soporte.objects.get(contrato = contrato,formador = contrato.formador,tipo = tipo)
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

        for soporte in contrato.soportes_requeridos.soportes_requeridos.filter(categoria = 'Seguridad Social').order_by('nombre'):

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

class CohortesFormadoresForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CohortesFormadoresForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Cohortes de contratación:',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('archivo',css_class='col-sm-6'),
                    Div('contratos',css_class='col-sm-6'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = CohortesFormadores
        fields = ['nombre','archivo','contratos']