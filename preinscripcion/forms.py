#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from preinscripcion.models import DocentesPreinscritos
from municipios.models import Municipio
from radicados.models import Radicado
from docentes.models import DocentesMinEducacion
from departamentos.models import Departamento
from municipios.models import Municipio

class Consulta(forms.Form):

    def __init__(self, *args, **kwargs):
        super(Consulta, self).__init__(*args, **kwargs)
        self.fields['cedula'].label = "Digita tu numero de cédula (sin puntos o comas)"
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    Div('cedula',css_class='col-sm-4 col-sm-offset-4'),
                    css_class = 'row'
                ),
                HTML("""
                <button type="submit" class="btn btn-cpe">Consultar</button>
                """)
            ),
        )

    cedula = forms.IntegerField(label='Cedula')

class Registro(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Registro, self).__init__(*args, **kwargs)
        docente = DocentesMinEducacion.objects.get(cedula=kwargs['initial']['cedula'])

        self.fields['primer_apellido'].initial = docente.primer_apellido
        self.fields['segundo_apellido'].initial = docente.segundo_apellido
        self.fields['primer_nombre'].initial = docente.primer_nombre
        self.fields['segundo_nombre'].initial = docente.segundo_nombre
        self.fields['cedula'].initial = docente.cedula
        self.fields['cargo'].initial = docente.cargo
        self.fields['verificado'].initial = True

        if 'data' not in kwargs:
            self.fields['municipio'].widget.choices = (('','---------'),)
            self.fields['radicado'].widget.choices = (('','---------'),)


        else:
            id_departamento = kwargs['data']['departamento']
            if id_departamento == '':
                id_departamento = 0
            self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

            id_municipio = kwargs['data']['municipio']
            if id_municipio == '':
                id_municipio = 0
            self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <p style="color:white;">Porfavor actualiza tus datos personales en el siguiente formulario:</p>
                <br>
                """),

                Div(
                    Div('primer_apellido',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_apellido',css_class='col-sm-4'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),



                Div(
                    Div('cedula',css_class='col-sm-4 col-sm-offset-2'),
                    Div('cargo',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-3 col-sm-offset-2'),
                    Div('telefono_fijo',css_class='col-sm-3'),
                    Div('telefono_celular',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('departamento',css_class='col-sm-3 col-sm-offset-2'),
                    Div('municipio',css_class='col-sm-3'),
                    Div('radicado',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),


                HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Preinscribirme</button></div>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo Docente','Directivo Docente')))
        }

class RegistroSedBogota(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistroSedBogota, self).__init__(*args, **kwargs)

        self.fields['departamento'].initial = Departamento.objects.get(id=10)
        self.fields['municipio'].initial = Municipio.objects.get(id=458)
        self.fields['docentes_innovadores'].initial = True

        try:
            docente = DocentesMinEducacion.objects.get(cedula=kwargs['initial']['cedula'])
        except:
            pass
        else:
            self.fields['primer_apellido'].initial = docente.primer_apellido
            self.fields['segundo_apellido'].initial = docente.segundo_apellido
            self.fields['primer_nombre'].initial = docente.primer_nombre
            self.fields['segundo_nombre'].initial = docente.segundo_nombre
            self.fields['cedula'].initial = docente.cedula
            self.fields['cargo'].initial = docente.cargo


        self.fields['radicado'].queryset = Radicado.objects.filter(municipio__id = 458)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <p style="color:white;">Porfavor actualiza tus datos personales en el siguiente formulario:</p>
                <br>
                """),

                Div(
                    Div('primer_apellido',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_apellido',css_class='col-sm-4'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),



                Div(
                    Div('cedula',css_class='col-sm-2 col-sm-offset-2'),
                    Div('cargo',css_class='col-sm-3'),
                    Div('area',css_class='col-sm-3'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-3 col-sm-offset-2'),
                    Div('telefono_fijo',css_class='col-sm-3'),
                    Div('telefono_celular',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('radicado',css_class='col-sm-4 col-sm-offset-2'),
                    Div('localidad',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    Div('departamento',css_class='col-sm-3 col-sm-offset-2'),
                    Div('municipio',css_class='col-sm-3 col-sm-offset-2'),
                    Div('docentes_innovadores',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),


                HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Inscribirme</button></div>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('','----------'),('Docente','Docente'),('Directivo Docente','Directivo Docente'))),
            'localidad':forms.Select(choices=sorted([('','----------'),('Usaquén','Usaquén'),('Chapinero','Chapinero'),
                                              ('Santa Fe','Santa Fe'),('San Cristóbal','San Cristóbal'),
                                              ('Usme','Usme'),('Tunjuelito','Tunjuelito'),
                                              ('Bosa','Bosa'),('Kennedy','Kennedy'),
                                              ('Fontibón','Fontibón'),('Engativá','Engativá'),
                                              ('Suba','Suba'),('Barrios Unidos','Barrios Unidos'),
                                              ('Teusaquillo','Teusaquillo'),('Los Mártires','Los Mártires'),
                                              ('Antonio Nariño','Antonio Nariño'),('Puente Aranda','Puente Aranda'),
                                              ('La Candelaria','La Candelaria'),('Rafael Uribe Uribe','Rafael Uribe Uribe'),
                                              ('Ciudad Bolívar','Ciudad Bolívar'),('Sumapaz','Sumapaz')])
                                    ),
            'area':forms.Select(choices=sorted([('','----------'),
                                                ('Ciencias naturales y educación ambiental','Ciencias naturales y educación ambiental'),
                                                ('Ciencias sociales, historia, geografia, constitución política y/o democrática','Ciencias sociales, historia, geografia, constitución política y/o democrática'),
                                                ('Educación artística','Educación artística'),
                                                ('Educación ética y en valores humanos','Educación ética y en valores humanos'),
                                                ('Educación física, recreación y deportes','Educación física, recreación y deportes'),
                                                ('Educación religiosa','Educación religiosa'),
                                                ('Humanidades','Humanidades'),
                                                ('Matemáticas','Matemáticas'),
                                                ('Lengua castellana','Lengua castellana'),
                                                ('Lengua extranjera: Inglés','Lengua extranjera: Inglés'),
                                                ('Lengua nativa','Lengua nativa'),
                                                ('Competencias ciudadanas','Competencias ciudadanas'),
                                                ('Filosofía','Filosofía'),
                                                ('Todas las áreas','Todas las áreas'),
                                                ])
                                ),
        }

class PregistroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PregistroForm, self).__init__(*args, **kwargs)

        self.fields['cedula'].initial = kwargs['initial']['cedula']
        self.fields['verificado'].initial = False

        if 'data' not in kwargs:
            self.fields['municipio'].widget.choices = (('','---------'),)
            self.fields['radicado'].widget.choices = (('','---------'),)

        else:
            id_departamento = kwargs['data']['departamento']
            if id_departamento == '':
                id_departamento = 0
            self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

            id_municipio = kwargs['data']['municipio']
            if id_municipio == '':
                id_municipio = 0
            self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <h3>No se ha encontrado tu numero de cedula en la base de datos de docentes.</h3>
                <p style="color:white;">Por favor completa el siguiente formulario para comprobar con la secretaria de educación
                tu vinculación.</p>
                <br>
                """),

                Div(
                    Div('primer_apellido',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_apellido',css_class='col-sm-4'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),



                Div(
                    Div('cedula',css_class='col-sm-4 col-sm-offset-2'),
                    Div('cargo',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-3 col-sm-offset-2'),
                    Div('telefono_fijo',css_class='col-sm-3'),
                    Div('telefono_celular',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('departamento',css_class='col-sm-3 col-sm-offset-2'),
                    Div('municipio',css_class='col-sm-3'),
                    Div('radicado',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),


                HTML("""
                <div class="row"><button type="submit" class="btn btn-cpe">Preinscribirme</button></div>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo Docente','Directivo Docente')))
        }

class UpdateRegistroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateRegistroForm, self).__init__(*args, **kwargs)
        id_departamento = self.initial['departamento']
        if id_departamento == '':
            id_departamento = 0
        self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

        id_municipio = self.initial['municipio']
        if id_municipio == '':
            id_municipio = 0
        self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',

                HTML("""
                <p style="color:white;">Si lo requieres actualiza tus datos personales en el siguiente formulario:</p>
                <br>
                """),

                Div(
                    Div('primer_apellido',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_apellido',css_class='col-sm-4'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-4 col-sm-offset-2'),
                    Div('segundo_nombre',css_class='col-sm-4'),
                    css_class = 'row'
                ),



                Div(
                    Div('cedula',css_class='col-sm-4 col-sm-offset-2'),
                    Div('cargo',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-3 col-sm-offset-2'),
                    Div('telefono_fijo',css_class='col-sm-3'),
                    Div('telefono_celular',css_class='col-sm-2'),
                    css_class = 'row'
                ),

                Div(
                    Div('departamento',css_class='col-sm-3 col-sm-offset-2'),
                    Div('municipio',css_class='col-sm-3'),
                    Div('radicado',css_class='col-sm-2'),
                    css_class = 'row'
                ),


                HTML("""
                <button type="submit" class="btn btn-cpe">Actualizar</button>
                """)
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo docente','Directivo docente')))
        }

class DocentesPreinscritosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DocentesPreinscritosForm, self).__init__(*args, **kwargs)

        if 'data' not in kwargs:
            self.fields['municipio'].widget.choices = (('','---------'),)
            self.fields['radicado'].widget.choices = (('','---------'),)


        else:
            id_departamento = kwargs['data']['departamento']
            if id_departamento == '':
                id_departamento = 0
            self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

            id_municipio = kwargs['data']['municipio']
            if id_municipio == '':
                id_municipio = 0
            self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Nueva preinscripción de docente:',

                Div(
                    Div('primer_apellido',css_class='col-sm-6'),
                    Div('segundo_apellido',css_class='col-sm-6'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-6'),
                    Div('segundo_nombre',css_class='col-sm-6'),
                    css_class = 'row'
                ),


                Div(
                    Div('cedula',css_class='col-sm-6'),
                    Div('cargo',css_class='col-sm-6'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-4'),
                    Div('telefono_fijo',css_class='col-sm-4'),
                    Div('telefono_celular',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('departamento',css_class='col-sm-4'),
                    Div('municipio',css_class='col-sm-4'),
                    Div('radicado',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo Docente','Directivo Docente')))
        }

class DocentesPreinscritosUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DocentesPreinscritosUpdateForm, self).__init__(*args, **kwargs)

        id_departamento = self.initial['departamento']
        if id_departamento == '':
            id_departamento = 0
        self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id=id_departamento).values_list('id','nombre')

        id_municipio = self.initial['municipio']
        if id_municipio == '':
            id_municipio = 0
        self.fields['radicado'].widget.choices = Radicado.objects.filter(municipio__id=id_municipio).values_list('id','nombre_sede')



        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Editar preinscripción:',

                Div(
                    Div('primer_apellido',css_class='col-sm-6'),
                    Div('segundo_apellido',css_class='col-sm-6'),
                    css_class = 'row'
                ),


                Div(
                    Div('primer_nombre',css_class='col-sm-6'),
                    Div('segundo_nombre',css_class='col-sm-6'),
                    css_class = 'row'
                ),


                Div(
                    Div('cedula',css_class='col-sm-6'),
                    Div('cargo',css_class='col-sm-6'),
                    css_class = 'row'
                ),

                Div(
                    Div('correo',css_class='col-sm-4'),
                    Div('telefono_fijo',css_class='col-sm-4'),
                    Div('telefono_celular',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('departamento',css_class='col-sm-4'),
                    Div('municipio',css_class='col-sm-4'),
                    Div('radicado',css_class='col-sm-4'),
                    css_class = 'row'
                ),

                Div(
                    Div('verificado',css_class='col-sm-3 col-sm-offset-2'),
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = DocentesPreinscritos
        fields = '__all__'
        widgets = {
            'cargo':forms.Select(choices=(('Docente','Docente'),('Directivo Docente','Directivo Docente')))
        }