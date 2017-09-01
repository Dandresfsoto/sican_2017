#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from matrices.models import Beneficiario
from region.models import Region
from productos.models import Diplomado
from radicados.models import Radicado
from formadores.models import Grupos, Formador
from matrices.models import CargaMasiva
from usuarios.models import User
from evidencias.models import Evidencia

class BeneficiarioForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(BeneficiarioForm, self).clean()
        radicado_text = cleaned_data.get('radicado_text')
        diplomado = cleaned_data.get('diplomado')
        area = cleaned_data.get('area')
        grado = cleaned_data.get('grado')

        if diplomado.nombre != 'ESCUELA TIC FAMILIA':
            if radicado_text == '':
                self.add_error('radicado_text','Este campo es requerido.')

            try:
                radicado = Radicado.objects.get(numero = radicado_text)
            except:
                radicado = ''

            if radicado == '':
                self.add_error('radicado_text','No existe este numero de radicado')

        else:
            pass


    def __init__(self, *args, **kwargs):
        super(BeneficiarioForm, self).__init__(*args, **kwargs)
        diplomado_nombre = kwargs['initial']['diplomado_nombre']

        if diplomado_nombre == 'INNOVATIC':
            numero = 1
        elif diplomado_nombre == 'TECNOTIC':
            numero = 2
        elif diplomado_nombre == 'DIRECTIC':
            numero = 3
        elif diplomado_nombre == 'ESCUELA TIC FAMILIA':
            numero = 4
        elif diplomado_nombre == 'ESCUELATIC':
            numero = 4
        else:
            numero = 0

        if numero == 4:
            self.fields['radicado_text'].widget = forms.HiddenInput()
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['grado'].widget = forms.HiddenInput()

        self.fields['grupo'].widget.choices = (('','----------'),)
        self.fields['diplomado'].initial = Diplomado.objects.get(numero=numero)

        if 'data' in kwargs.keys():
            if kwargs['data']['formador'] != '':
                formador = Formador.objects.get(id=kwargs['data']['formador'])
                choices = []
                for choice in Grupos.objects.filter(formador=formador):
                    choices.append((choice.id,choice.formador.codigo_ruta + '-' + choice.nombre))
                self.fields['grupo'].choices = choices


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos Generales',
                Div(
                    Div('diplomado',css_class='col-sm-4'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('region',css_class='col-sm-4'),
                    Div('formador',css_class='col-sm-4'),
                    Div('grupo',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('radicado_text',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Datos personales',
                Div(
                    Div('apellidos',css_class='col-sm-4'),
                    Div('nombres',css_class='col-sm-4'),
                    Div('cedula',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('correo',css_class='col-sm-4'),
                    Div('telefono_fijo',css_class='col-sm-4'),
                    Div('telefono_celular',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('area',css_class='col-sm-6'),
                    Div('grado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('genero',css_class='col-sm-6'),
                    Div('estado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Beneficiario
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=(('','----------'),('Activo','Activo'),('Conformación de grupo','Conformación de grupo'),('Retirado','Retirado'))),
            'genero': forms.Select(choices=(('','----------'),('Femenino','Femenino'),('Masculino','Masculino')))
        }
        labels = {
            'radicado_text': 'Radicado*',
            'area':'Area',
            'grado':'Grado'
        }

class BeneficiarioUpdateForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(BeneficiarioUpdateForm, self).clean()
        radicado_text = cleaned_data.get('radicado_text')
        diplomado = cleaned_data.get('diplomado')
        area = cleaned_data.get('area')
        grado = cleaned_data.get('grado')

        if diplomado.nombre != u'ESCUELA TIC FAMILIA' and diplomado.nombre != u'ESCUELATIC':
            if radicado_text == '':
                self.add_error('radicado_text','Este campo es requerido.')

            try:
                radicado = Radicado.objects.get(numero = radicado_text)
            except:
                radicado = ''

            if radicado == '':
                self.add_error('radicado_text','No existe este numero de radicado')

        else:
            pass

    def __init__(self, *args, **kwargs):
        super(BeneficiarioUpdateForm, self).__init__(*args, **kwargs)
        diplomado_nombre = kwargs['initial']['diplomado_nombre']

        if diplomado_nombre == 'INNOVATIC':
            numero = 1
        elif diplomado_nombre == 'TECNOTIC':
            numero = 2
        elif diplomado_nombre == 'DIRECTIC':
            numero = 3
        elif diplomado_nombre == 'ESCUELA TIC FAMILIA':
            numero = 4
        elif diplomado_nombre == 'ESCUELATIC':
            numero = 4
        else:
            numero = 0

        if numero == 4:
            self.fields['radicado_text'].widget = forms.HiddenInput()
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['grado'].widget = forms.HiddenInput()

        self.fields['grupo'].widget.choices = (('','----------'),)
        self.fields['diplomado'].initial = Diplomado.objects.get(numero=numero)

        formador = Formador.objects.get(id=kwargs['initial']['formador_id'])
        choices = []
        for choice in Grupos.objects.filter(formador=formador):
            choices.append((choice.id,choice.formador.codigo_ruta + '-' + choice.nombre))
        self.fields['grupo'].choices = choices


        if 'data' in kwargs.keys():
            if kwargs['data']['formador'] != '':
                formador = Formador.objects.get(id=kwargs['data']['formador'])
                choices = []
                for choice in Grupos.objects.filter(formador=formador):
                    choices.append((choice.id,choice.formador.codigo_ruta + '-' + choice.nombre))
                self.fields['grupo'].choices = choices


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos Generales',
                Div(
                    Div('diplomado',css_class='col-sm-4'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('region',css_class='col-sm-4'),
                    Div('formador',css_class='col-sm-4'),
                    Div('grupo',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('radicado_text',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Datos personales',
                Div(
                    Div('apellidos',css_class='col-sm-4'),
                    Div('nombres',css_class='col-sm-4'),
                    Div('cedula',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('correo',css_class='col-sm-4'),
                    Div('telefono_fijo',css_class='col-sm-4'),
                    Div('telefono_celular',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('area',css_class='col-sm-6'),
                    Div('grado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('genero',css_class='col-sm-6'),
                    Div('estado',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Beneficiario
        fields = '__all__'
        widgets = {
            'estado': forms.Select(choices=(('','----------'),('Activo','Activo'),('Conformación de grupo','Conformación de grupo'),('Retirado','Retirado'))),
            'genero': forms.Select(choices=(('','----------'),('Femenino','Femenino'),('Masculino','Masculino')))
        }
        labels = {
            'radicado_text': 'Radicado*',
            'area':'Area',
            'grado':'Grado'
        }

class CargaMasivaForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(CargaMasivaForm, self).clean()
        archivo = cleaned_data.get('archivo')
        if archivo.content_type != u'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            self.add_error('archivo','Se debe seleccionar un archivo excel.')


    def __init__(self, *args, **kwargs):
        super(CargaMasivaForm, self).__init__(*args, **kwargs)

        self.fields['usuario'].initial = User.objects.get(id = kwargs['initial']['id_usuario'])
        self.fields['usuario'].widget = forms.HiddenInput()

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Carga masiva de matrices',
                Div(
                    HTML("""
                            <file-upload-sican style="margin-left:14px;" name="archivo">Archivo</file-upload-sican>
                        """),
                    css_class = 'row'
                ),
                Div(
                    'archivo',
                    css_class = 'hidden'
                )
            ),
        )

    class Meta:
        model = CargaMasiva
        fields = ['usuario','archivo']

class PleBeneficiarioForm(forms.Form):

    nombre = forms.CharField(label='Nombre del PLE',max_length=100)
    para_leer = forms.CharField(label='Sección "PARA LEER"',max_length=10000,widget=forms.Textarea())
    imagen_para_leer = forms.ImageField(required=False)

    para_hacer_1 = forms.URLField(label='Link "PARA HACER"',max_length=200)
    para_hacer_2 = forms.URLField(label='Link "PARA HACER"',max_length=200,required=False)
    para_hacer_3 = forms.URLField(label='Link "PARA HACER"',max_length=200,required=False)
    para_hacer_4 = forms.URLField(label='Link "PARA HACER"',max_length=200,required=False)

    imagen_historieta = forms.ImageField()
    imagen_infografia = forms.ImageField()
    imagen_graficacion_ple = forms.ImageField()
    link_ruta_sostenibilidad = forms.URLField(max_length=200)

    area = forms.CharField(max_length=100,widget=forms.Select(choices=[
        ('','----------'),
        ('1','Ciencias naturales y educación ambiental'),
        ('2','Ciencias sociales, historia, geografía, constitución política y/o deocrática'),
        ('3','Educación artística'),
        ('4','Educación ética y en valores humanos'),
        ('5','Educación física, recreación y deportes'),
        ('6','Educación religiosa'),
        ('7','Humanidades'),
        ('8','Matemáticas'),
        ('9','Lengua castellana'),
        ('10','Lengua extranjera: Inglés'),
        ('11','Lengua nativa'),
        ('12','Competencias Ciudadanas'),
        ('13','Filosofía'),
        ('14','Todas las áreas')
    ]))


    def __init__(self, *args, **kwargs):
        super(PleBeneficiarioForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].initial = kwargs['initial']['beneficiario'].nombre_producto_final
        self.fields['para_leer'].initial = kwargs['initial']['beneficiario'].para_leer
        self.fields['imagen_para_leer'].initial = kwargs['initial']['beneficiario'].imagen_para_leer

        self.fields['para_hacer_1'].initial = kwargs['initial']['beneficiario'].para_hacer_1
        self.fields['para_hacer_2'].initial = kwargs['initial']['beneficiario'].para_hacer_2
        self.fields['para_hacer_3'].initial = kwargs['initial']['beneficiario'].para_hacer_3
        self.fields['para_hacer_4'].initial = kwargs['initial']['beneficiario'].para_hacer_4

        self.fields['imagen_historieta'].initial = kwargs['initial']['beneficiario'].imagen_historieta
        self.fields['imagen_infografia'].initial = kwargs['initial']['beneficiario'].imagen_infografia
        self.fields['imagen_graficacion_ple'].initial = kwargs['initial']['beneficiario'].imagen_graficacion_ple
        self.fields['link_ruta_sostenibilidad'].initial = kwargs['initial']['beneficiario'].link_ruta_sostenibilidad

        self.fields['area'].initial = kwargs['initial']['beneficiario'].area_basica_producto_final


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Construcción del PLE',
                Div(
                    Div('nombre', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('area', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('para_leer', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('imagen_para_leer', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('para_hacer_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('para_hacer_2', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('para_hacer_3', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('para_hacer_4', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('imagen_historieta', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('imagen_infografia', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('imagen_graficacion_ple', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('link_ruta_sostenibilidad', css_class='col-sm-12'),
                    css_class='row'
                ),
            ),
        )