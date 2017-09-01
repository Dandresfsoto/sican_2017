#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm, Form
from django import forms
from usuarios.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from permisos_sican.models import UserPermissionSican
from crispy_forms.bootstrap import TabHolder, Tab
from departamentos.models import Departamento
from municipios.models import Municipio

class UserUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        user = User.objects.get(id = kwargs['initial']['id_user'])

        self.helper = FormHelper(self)

        municipios = [('','----------')]
        municipios_residencia = [('','----------')]
        municipios_residencia_temporal = [('','----------')]

        if 'data' in kwargs.keys():
            if kwargs['data']['departamento_natal'] != '':
                choices = Municipio.objects.filter(departamento__id = kwargs['data']['departamento_natal']).values_list('id','nombre')
                for choice in choices:
                    municipios.append(choice)

            if kwargs['data']['departamento_residencia'] != '':
                choices_residencia = Municipio.objects.filter(departamento__id = kwargs['data']['departamento_residencia']).values_list('id','nombre')
                for choice_residencia in choices_residencia:
                    municipios.append(choice_residencia)

            if kwargs['data']['departamento_residencia_temporal'] != '':
                choices_residencia_temporal = Municipio.objects.filter(departamento__id = kwargs['data']['departamento_residencia_temporal']).values_list('id','nombre')
                for choice_residencia_temporal in choices_residencia_temporal:
                    municipios.append(choice_residencia_temporal)

        else:
            if user.departamento_natal != None:
                choices = Municipio.objects.filter(departamento__id = user.departamento_natal.id).values_list('id','nombre')

                for choice in choices:
                    municipios.append(choice)

            if user.departamento_residencia != None:
                choices = Municipio.objects.filter(departamento__id = user.departamento_residencia.id).values_list('id','nombre')

                for choice in choices:
                    municipios_residencia.append(choice)

            if user.departamento_residencia_temporal != None:
                choices = Municipio.objects.filter(departamento__id = user.departamento_residencia_temporal.id).values_list('id','nombre')

                for choice in choices:
                    municipios_residencia_temporal.append(choice)

        self.fields['municipio_natal'].widget.choices = municipios
        self.fields['municipio_residencia'].widget.choices = municipios_residencia
        self.fields['municipio_residencia_temporal'].widget.choices = municipios_residencia_temporal

        self.helper.layout = Layout(
            TabHolder(
                Tab('Datos generales',
                    HTML(
                        """
                        <p></p>
                        """
                    ),
                    Div(
                        Div(
                            Div(
                                Div(
                                    Div('photo',css_class='col-sm-12'),
                                    css_class="row"
                                ),
                                css_class='col-sm-5'
                            ),
                            Div(
                                Div(
                                    HTML(
                                        """
                                        <div class="col-sm-12 margin-bottom-space">
                                            <p class="inline" style="font-weight:700;">Cargo:</p>
                                            <p class="inline">{{cargo}}</p>
                                        </div>
                                        """
                                    ),
                                    css_class="row"
                                ),
                                Div(
                                    HTML(
                                        """
                                        <div class="col-sm-12 margin-bottom-space">
                                            <p class="inline" style="font-weight:700;">Número de contrato:</p>
                                            <p class="inline">{{numero_contrato}}</p>
                                        </div>
                                        """
                                    ),
                                    css_class="row"
                                ),
                                Div(
                                    HTML(
                                        """
                                        <div class="col-sm-12 margin-bottom-space">
                                            <p class="inline" style="font-weight:700;">Fecha de inicio:</p>
                                            <p class="inline">{{fecha_inicio}}</p>
                                        </div>
                                        """
                                    ),
                                    css_class="row"
                                ),
                                Div(
                                    HTML(
                                        """
                                        <div class="col-sm-12 margin-bottom-space">
                                            <p class="inline" style="font-weight:700;">Fecha de terminación:</p>
                                            <p class="inline">{{fecha_terminacion}}</p>
                                        </div>
                                        """
                                    ),
                                    css_class="row"
                                ),
                                Div(
                                    Div('first_name',css_class='col-sm-6'),
                                    Div('last_name',css_class='col-sm-6'),
                                    css_class="row"
                                ),
                                Div(
                                    Div('fecha_nacimiento',css_class='col-sm-4'),
                                    Div('departamento_natal',css_class='col-sm-4'),
                                    Div('municipio_natal',css_class='col-sm-4'),
                                    css_class="row"
                                ),
                                Div(
                                    Div('cedula',css_class='col-sm-4'),
                                    Div('genero',css_class='col-sm-4'),
                                    Div('tipo_sangre',css_class='col-sm-4'),
                                    css_class="row"
                                ),
                                css_class='col-sm-7'
                            ),

                            css_class = 'row'
                        ),
                        css_class = 'container-fluid'
                    ),
                ),
                Tab('Contacto',
                    HTML(
                        """
                        <p></p>
                        """
                    ),
                    Div(
                        Div(
                            Div(

                                Div(
                                    Div(
                                        HTML("""
                                        <i class="fa fa-envelope fa-2x" aria-hidden="true"></i>
                                        """)
                                        ,css_class='col-sm-1'
                                    ),
                                    Div(
                                        Div('correo_personal')
                                        ,css_class='col-sm-11'
                                    )
                                ),
                                css_class='col-sm-6'
                            ),
                            Div(

                                Div(
                                    Div(
                                        HTML("""
                                        <i class="fa fa-mobile fa-2x" aria-hidden="true"></i>
                                        """)
                                        ,css_class='col-sm-1'
                                    ),
                                    Div(
                                        Div('telefono_personal')
                                        ,css_class='col-sm-11'
                                    )
                                ),
                                css_class='col-sm-6'
                            ),

                            css_class = 'row'
                        ),


                        Div(
                            Div(

                                Div(
                                    Div(
                                        HTML("""
                                        <i class="fa fa-skype fa-2x" aria-hidden="true"></i>
                                        """)
                                        ,css_class='col-sm-1'
                                    ),
                                    Div(
                                        Div('skype')
                                        ,css_class='col-sm-11'
                                    )
                                ),
                                css_class='col-sm-6'
                            ),
                            Div(

                                Div(
                                    Div(
                                        HTML("""
                                        <i class="fa fa-whatsapp fa-2x" aria-hidden="true"></i>
                                        """)
                                        ,css_class='col-sm-1'
                                    ),
                                    Div(
                                        Div('whatsapp')
                                        ,css_class='col-sm-11'
                                    )
                                ),
                                css_class='col-sm-6'
                            ),

                            css_class = 'row'
                        ),



                        Div(
                            Div(

                                Div(
                                    Div(
                                        HTML("""
                                        <i class="fa fa-facebook-official fa-2x" aria-hidden="true"></i>
                                        """)
                                        ,css_class='col-sm-1'
                                    ),
                                    Div(
                                        Div('facebook')
                                        ,css_class='col-sm-11'
                                    )
                                ),
                                css_class='col-sm-6'
                            ),
                            Div(

                                Div(
                                    Div(
                                        HTML("""
                                        <i class="fa fa-twitter fa-2x" aria-hidden="true"></i>
                                        """)
                                        ,css_class='col-sm-1'
                                    ),
                                    Div(
                                        Div('twitter')
                                        ,css_class='col-sm-11'
                                    )
                                ),
                                css_class='col-sm-6'
                            ),

                            css_class = 'row'
                        ),


                        css_class = 'container-fluid'
                    ),
                ),
                Tab('Residencia permanente',
                    HTML(
                        """
                        <p></p>
                        """
                    ),
                    Div(
                        Div(
                            Div('departamento_residencia',css_class='col-sm-4'),
                            Div('municipio_residencia',css_class='col-sm-4'),
                            Div('direccion_residencia',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        Div(
                            Div('barrio_residencia',css_class='col-sm-4'),
                            Div('telefono_residencia',css_class='col-sm-4'),
                            Div('celular_residencia',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        Div(
                            Div('nombre_contacto_residencia',css_class='col-sm-4'),
                            Div('telefono_contacto_residencia',css_class='col-sm-4'),
                            Div('celular_contacto_residencia',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        css_class = 'container-fluid'
                    ),
                    HTML(
                        """
                        <p>*La residencia permanente hace referencia a tu lugar original de radicación y vivienda.</p>
                        """
                    ),
                ),
                Tab('Residencia temporal',
                    HTML(
                        """
                        <p></p>
                        """
                    ),
                    Div(
                        Div(
                            Div('departamento_residencia_temporal',css_class='col-sm-4'),
                            Div('municipio_residencia_temporal',css_class='col-sm-4'),
                            Div('direccion_residencia_temporal',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        Div(
                            Div('barrio_residencia_temporal',css_class='col-sm-4'),
                            Div('telefono_residencia_temporal',css_class='col-sm-4'),
                            Div('celular_residencia_temporal',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        Div(
                            Div('nombre_contacto_residencia_temporal',css_class='col-sm-4'),
                            Div('telefono_contacto_residencia_temporal',css_class='col-sm-4'),
                            Div('celular_contacto_residencia_temporal',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        css_class = 'container-fluid'
                    ),
                    HTML(
                        """
                        <p>*Si tuviste que cambiar de residencia de manera temporal para la ejecución del contrato por
                        favor diligencia este formulario.</p>
                        """
                    ),
                ),
                Tab('Transporte a capital',
                    HTML(
                        """
                        <p></p>
                        """
                    ),
                    Div(
                        Div(
                            Div('empresa_transporte',css_class='col-sm-4'),
                            Div('tiempo_transporte',css_class='col-sm-4'),
                            Div('valor_transporte',css_class='col-sm-4'),
                            css_class="row"
                        ),
                        Div(
                            Div('horarios_transporte',css_class='col-sm-12'),
                            css_class="row"
                        ),
                        css_class = 'container-fluid'
                    ),
                    HTML(
                        """
                        <p>*Ingresa la información de transporte desde tu sitio de residencia temporal o permanente hasta la
                        capital del departamento.</p>
                        """
                    ),
                ),

                Tab('Información adicional',
                    HTML(
                        """
                        <p></p>
                        """
                    ),
                    Div(
                        Div(
                            Div('informacion_adicional',css_class='col-sm-12'),
                            css_class="row"
                        ),
                        css_class = 'container-fluid'
                    ),
                    HTML(
                        """
                        <p>*Si necesitas agregar alguna observación adicional de contacto, usa este espacio.</p>
                        """
                    ),
                )
            )
        )

    class Meta:
        model = User
        fields = ['first_name','last_name','telefono_personal','correo_personal','photo','fecha_nacimiento',
                  'departamento_natal','municipio_natal','cedula','genero','tipo_sangre','skype','whatsapp',
                  'facebook','twitter','departamento_residencia','municipio_residencia','direccion_residencia',
                  'barrio_residencia','telefono_residencia','celular_residencia','nombre_contacto_residencia',
                  'telefono_contacto_residencia','celular_contacto_residencia','departamento_residencia_temporal',
                  'municipio_residencia_temporal','direccion_residencia_temporal',
                  'barrio_residencia_temporal','telefono_residencia_temporal','celular_residencia_temporal',
                  'nombre_contacto_residencia_temporal',
                  'telefono_contacto_residencia_temporal','celular_contacto_residencia_temporal',
                  'empresa_transporte','horarios_transporte','tiempo_transporte','valor_transporte','informacion_adicional']

        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo corporativo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'departamento_natal': 'Departamento natal',
            'municipio_natal': 'Municipio natal',
            'photo': 'Fotografia',
            'departamento_residencia':'Departamento',
            'municipio_residencia':'Municipio',
            'direccion_residencia':'Dirección',
            'barrio_residencia':'Barrio',
            'telefono_residencia':'Teléfono',
            'celular_residencia':'Celular',
            'nombre_contacto_residencia':'Persona de contacto',
            'telefono_contacto_residencia':'Teléfono',
            'celular_contacto_residencia':'Celular',
            'departamento_residencia_temporal':'Departamento',
            'municipio_residencia_temporal':'Municipio',
            'direccion_residencia_temporal':'Dirección',
            'barrio_residencia_temporal':'Barrio',
            'telefono_residencia_temporal':'Teléfono',
            'celular_residencia_temporal':'Celular',
            'nombre_contacto_residencia_temporal':'Persona de contacto',
            'telefono_contacto_residencia_temporal':'Teléfono',
            'celular_contacto_residencia_temporal':'Celular',
            'empresa_transporte':'Nombre de la transportadora',
            'horarios_transporte':'Horarios de despacho',
            'tiempo_transporte':'Tiempo aproximado',
            'valor_transporte':'Valor ($)',
            'informacion_adicional':'Información adicional'
        }

        widgets = {
            'email': forms.EmailInput(attrs={'readonly':True}),
            'cargo': forms.Select(attrs={'readonly':True}),
            'genero': forms.Select(choices=[('','------------'),('Femenino','Femenino'),('Masculino','Masculino')]),
            'tipo_sangre': forms.Select(choices=[('','------------'),('AB+','AB+'),('AB-','AB-'),('A+','A+'),('A-','A-'),
                                                 ('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-')])
        }

class UserNewAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserNewAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos personales',
                Div(
                    Div('email',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('first_name',css_class='col-sm-6'),
                    Div('last_name',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('telefono_personal',css_class='col-sm-6'),
                    Div('correo_personal',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),

            Fieldset(
                'Cuenta de usuario',
                Div(
                    Div('cargo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('groups',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('is_active',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = User
        fields = ['email','first_name','last_name','telefono_personal','correo_personal','cargo','is_active','groups']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'is_active': 'Activo',
        }
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'checked':''})
        }

class UserUpdateAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserUpdateAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Datos personales',
                Div(
                    Div('first_name',css_class='col-sm-6'),
                    Div('last_name',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('telefono_personal',css_class='col-sm-6'),
                    Div('correo_personal',css_class='col-sm-6'),
                    css_class = 'row'
                ),
            ),

            Fieldset(
                'Cuenta de usuario',
                Div(
                    Div('cargo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('groups',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('is_active',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = User
        fields = ['first_name','last_name','telefono_personal','correo_personal','cargo','is_active','groups']
        labels = {
            'first_name': 'Nombre(s)',
            'last_name': 'Apellidos',
            'email': 'Correo corporativo',
            'is_active': 'Activo'
        }

        widgets = {
        }

class GroupNewAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupNewAdminForm, self).__init__(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(UserPermissionSican)
        exclude_perms = ['add_userpermissionsican','change_userpermissionsican','delete_userpermissionsican']
        self.fields['permissions'].queryset = Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del grupo:',
                Div(
                    Div('name',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('permissions',css_class='col-sm-12'),
                    css_class = 'row'
                ),
            ),
        )

    class Meta:
        model = Group
        fields = '__all__'

        widget = {
        }

class ChangePasswordForm(Form):

    previus_password = forms.CharField(label='Contraseña anterior',max_length=100, widget=forms.PasswordInput())
    new_password_1 = forms.CharField(label='Nueva contraseña',max_length=100, widget=forms.PasswordInput())
    new_password_2 = forms.CharField(label='Repita la nueva contraseña',max_length=100, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.user = kwargs['initial']['user']
        self.helper.layout = Layout(
            Fieldset(
                'Cambio de contraseña:',
                Div(
                    Div('previus_password',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('new_password_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('new_password_2',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
        )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        previus_password = cleaned_data.get('previus_password')
        new_password_1 = cleaned_data.get('new_password_1')
        new_password_2 = cleaned_data.get('new_password_2')
        user = authenticate(email=self.user.email, password=previus_password)

        if user is None:
            self.add_error('previus_password','La contraseña no es correcta.')


        if new_password_1 != new_password_2:
            self.add_error('new_password_1',"Los campos de la nueva contraseña no coinciden.")
            self.add_error('new_password_2',"Los campos de la nueva contraseña no coinciden.")

class NuevoPermisoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NuevoPermisoForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].initial = ContentType.objects.get_for_model(UserPermissionSican)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del permiso:',
                Div(
                    Div('name',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('codename',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    Div('content_type',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
            ),
        )

    class Meta:
        model = Permission
        fields = '__all__'
        labels = {
            'codename': 'Codigo'
        }
        widget = {
        }