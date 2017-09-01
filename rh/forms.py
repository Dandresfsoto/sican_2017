#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from rh.models import TipoSoporte, RequerimientoPersonal
from usuarios.models import User
from municipios.models import Municipio

class NuevoTipoSoporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NuevoTipoSoporteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Tipo de soporte RH',
                Div(
                    Div('nombre',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('categoria',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = TipoSoporte
        fields = '__all__'
        widgets = {'categoria':forms.Select(choices=[('','----------'),('General','General'),('Seguridad Social','Seguridad Social')])}

class RequerimientoPersonalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoPersonalForm, self).__init__(*args, **kwargs)
        queryset = User.objects.filter(email__istartswith = 'lider')
        user = User.objects.get(id = kwargs['initial']['user_id'])

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento'] != '':
                self.fields['municipios'].choices = Municipio.objects.filter(departamento__id=kwargs['data']['departamento']).values_list('id','nombre')
            else:
                self.fields['municipios'].choices = [('','---------------')]
        else:
            self.fields['municipios'].choices = [('','---------------')]

        self.fields['solicitante'].initial = user


        self.fields['encargado'].queryset = queryset

        if user.id in queryset.values_list('id',flat=True):
            self.fields['encargado'].initial = user
            self.fields['encargado'].widget = forms.HiddenInput()


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'REQUERIMIENTO DE CONTRATACIÓN',
                Div('solicitante',css_class='hidden'),
                Div(
                    Div('departamento',css_class='col-sm-4'),
                    Div('municipios',css_class='col-sm-8'),
                    css_class = 'row'
                ),
                Div(
                    Div('codigo_ruta',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('encargado',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('observacion_solicitante',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )
    class Meta:
        model = RequerimientoPersonal
        fields = ['solicitante','encargado','departamento','municipios','codigo_ruta','observacion_solicitante']

class RequerimientoPersonalRh(forms.ModelForm):

    def clean(self):
        cleaned_data = super(RequerimientoPersonalRh, self).clean()
        nombre = cleaned_data.get('nombre')
        cedula = cleaned_data.get('cedula')
        celular = cleaned_data.get('celular')
        email = cleaned_data.get('email')
        hv = cleaned_data.get('hv')
        observacion_respuesta = cleaned_data.get('observacion_respuesta')

        if nombre == "":
            self.add_error('nombre','Este campo es requerido.')
        if cedula == "":
            self.add_error('cedula','Este campo es requerido.')
        if celular == "":
            self.add_error('celular','Este campo es requerido.')
        if email == "":
            self.add_error('email','Este campo es requerido.')


    def __init__(self, *args, **kwargs):
        super(RequerimientoPersonalRh, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'REQUERIMIENTO DE CONTRATACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud}}</p></p>
                            <p class="inline bold-p">Encargado: <p class="inline">{{object.encargado.first_name}} {{object.encargado.last_name}}</p></p>
                            <p class="inline bold-p">Departamento: <p class="inline">{{object.departamento.nombre}}</p></p>
                            <p class="inline bold-p">Municipios: <p class="inline">{{object.get_municipios_string}}</p></p>
                            <p class="inline bold-p">Código ruta: <p class="inline">{{object.codigo_ruta}}</p></p>
                            <p class="inline bold-p">Observación solicitante: <p class="inline">{{object.observacion_solicitante}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'RESPUESTA RH',
                Div('solicitante',css_class='hidden'),
                Div(
                    Div('nombre',css_class='col-sm-8'),
                    Div('cedula',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('celular',css_class='col-sm-6'),
                    Div('email',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="hv" old_file="{{old_file}}"
                            link_old_file="{{link_old_file}}">Archivo</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
                Div(
                    Div('observacion_respuesta',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div('hv',css_class='hidden'),
            )
        )
    class Meta:
        model = RequerimientoPersonal
        fields = ['nombre','cedula','celular','email','hv','observacion_respuesta']

class RequerimientoPersonalRhCapacitado(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoPersonalRhCapacitado, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'REQUERIMIENTO DE CONTRATACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud}}</p></p>
                            <p class="inline bold-p">Encargado: <p class="inline">{{object.encargado.first_name}} {{object.encargado.last_name}}</p></p>
                            <p class="inline bold-p">Departamento: <p class="inline">{{object.departamento.nombre}}</p></p>
                            <p class="inline bold-p">Municipios: <p class="inline">{{object.get_municipios_string}}</p></p>
                            <p class="inline bold-p">Código ruta: <p class="inline">{{object.codigo_ruta}}</p></p>
                            <p class="inline bold-p">Observación solicitante: <p class="inline">{{object.observacion_solicitante}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'RESPUESTA RH',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_respuesta}}</p></p>
                            <p class="inline bold-p">Cedula: <p class="inline">{{object.nombre}}</p></p>
                            <p class="inline bold-p">Celular: <p class="inline">{{object.celular}}</p></p>
                            <p class="inline bold-p">Email: <p class="inline">{{object.email}}</p></p>
                            <p class="inline bold-p">Hoja de vida: <a href={{object.get_archivo_url}}><p class="inline">{{object.archivo_filename}}</p></a></p>
                            <p class="inline bold-p">Observación: <p class="inline">{{object.observacion_respuesta}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'CAPACITACIÓN',

                Div(
                    HTML("""
                            <p class="inline">Atención: Solo seleccione una de las opciones al finalizar el proceso de capacitación.</p>
                            <p></p>
                        """),
                    css_class = ''
                ),

                Div(
                    Div('contratar',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('observacion_final',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )
    contratar = forms.CharField(label='Proceso de capacitación',max_length=100,widget=forms.Select(choices=(('','----------'),
                                                                                                            ('contratar','Proceder a contratación'),
                                                                                                            ('desierto','El aspirante no continua con el proceso'),
                                                                                                            )))
    class Meta:
        model = RequerimientoPersonal
        fields = ['observacion_final']

class RequerimientoPersonalRhEspera(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoPersonalRhEspera, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'REQUERIMIENTO DE CONTRATACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud}}</p></p>
                            <p class="inline bold-p">Encargado: <p class="inline">{{object.encargado.first_name}} {{object.encargado.last_name}}</p></p>
                            <p class="inline bold-p">Departamento: <p class="inline">{{object.departamento.nombre}}</p></p>
                            <p class="inline bold-p">Municipios: <p class="inline">{{object.get_municipios_string}}</p></p>
                            <p class="inline bold-p">Código ruta: <p class="inline">{{object.codigo_ruta}}</p></p>
                            <p class="inline bold-p">Observación solicitante: <p class="inline">{{object.observacion_solicitante}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'RESPUESTA RH',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_respuesta}}</p></p>
                            <p class="inline bold-p">Cedula: <p class="inline">{{object.nombre}}</p></p>
                            <p class="inline bold-p">Celular: <p class="inline">{{object.celular}}</p></p>
                            <p class="inline bold-p">Email: <p class="inline">{{object.email}}</p></p>
                            <p class="inline bold-p">Hoja de vida: <a href={{object.get_archivo_url}}><p class="inline">{{object.archivo_filename}}</p></a></p>
                            <p class="inline bold-p">Observación: <p class="inline">{{object.observacion_respuesta}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'CAPACITACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">Pendiente</p></p>
                            <p class="inline bold-p">Observación: <p class="inline">Pendiente</p></p>
                            <p class="inline bold-p">Estado: <p class="inline">Esperando solicitud de contratación por parte del encargado</p></p>
                        """),
                    css_class = ''
                ),
            ),
        )

    class Meta:
        model = RequerimientoPersonal
        fields = []

class RequerimientoPersonalRhDeserta(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoPersonalRhDeserta, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'REQUERIMIENTO DE CONTRATACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud}}</p></p>
                            <p class="inline bold-p">Encargado: <p class="inline">{{object.encargado.first_name}} {{object.encargado.last_name}}</p></p>
                            <p class="inline bold-p">Departamento: <p class="inline">{{object.departamento.nombre}}</p></p>
                            <p class="inline bold-p">Municipios: <p class="inline">{{object.get_municipios_string}}</p></p>
                            <p class="inline bold-p">Código ruta: <p class="inline">{{object.codigo_ruta}}</p></p>
                            <p class="inline bold-p">Observación solicitante: <p class="inline">{{object.observacion_solicitante}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'RESPUESTA RH',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_respuesta}}</p></p>
                            <p class="inline bold-p">Cedula: <p class="inline">{{object.nombre}}</p></p>
                            <p class="inline bold-p">Celular: <p class="inline">{{object.celular}}</p></p>
                            <p class="inline bold-p">Email: <p class="inline">{{object.email}}</p></p>
                            <p class="inline bold-p">Hoja de vida: <a href={{object.get_archivo_url}}><p class="inline">{{object.archivo_filename}}</p></a></p>
                            <p class="inline bold-p">Observación: <p class="inline">{{object.observacion_respuesta}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'CAPACITACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud_contratacion}}</p></p>
                            <p class="inline bold-p">Observación: <p class="inline">{{object.observacion_final}}</p></p>
                            <p class="inline bold-p">Estado: <p class="inline">El aspirante no continua con el proceso</p></p>
                        """),
                    css_class = ''
                ),
            ),
        )

    class Meta:
        model = RequerimientoPersonal
        fields = []

class RequerimientoPersonalRhContratar(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RequerimientoPersonalRhContratar, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'REQUERIMIENTO DE CONTRATACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud}}</p></p>
                            <p class="inline bold-p">Encargado: <p class="inline">{{object.encargado.first_name}} {{object.encargado.last_name}}</p></p>
                            <p class="inline bold-p">Departamento: <p class="inline">{{object.departamento.nombre}}</p></p>
                            <p class="inline bold-p">Municipios: <p class="inline">{{object.get_municipios_string}}</p></p>
                            <p class="inline bold-p">Código ruta: <p class="inline">{{object.codigo_ruta}}</p></p>
                            <p class="inline bold-p">Observación solicitante: <p class="inline">{{object.observacion_solicitante}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'RESPUESTA RH',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_respuesta}}</p></p>
                            <p class="inline bold-p">Cedula: <p class="inline">{{object.nombre}}</p></p>
                            <p class="inline bold-p">Celular: <p class="inline">{{object.celular}}</p></p>
                            <p class="inline bold-p">Email: <p class="inline">{{object.email}}</p></p>
                            <p class="inline bold-p">Hoja de vida: <a href={{object.get_archivo_url}}><p class="inline">{{object.archivo_filename}}</p></a></p>
                            <p class="inline bold-p">Observación: <p class="inline">{{object.observacion_respuesta}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'CAPACITACIÓN',

                Div(
                    HTML("""
                            <p class="inline bold-p">Requerimiento: <p class="inline">REQ - {{object.id}}</p></p>
                            <p class="inline bold-p">Fecha: <p class="inline">{{object.fecha_solicitud_contratacion}}</p></p>
                            <p class="inline bold-p">Observación: <p class="inline">{{object.observacion_final}}</p></p>
                        """),
                    css_class = ''
                ),
            ),
            Fieldset(
                'CONTRATO',

                Div(
                    Div('contratado',css_class='col-sm-6'),
                    Div('contrato_enviado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
        )
    class Meta:
        model = RequerimientoPersonal
        fields = ['contratado','contrato_enviado']