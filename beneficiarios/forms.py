#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from beneficiarios.models import GruposBeneficiarios, BeneficiarioVigencia
from beneficiarios.models import Contrato
from radicados.models import Radicado


class GruposBeneficiariosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GruposBeneficiariosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['numero'].initial = GruposBeneficiarios.objects.filter(usuario = kwargs['initial']['user']).count() + 1
        self.fields['usuario'].initial = kwargs['initial']['user']
        self.fields['contrato'].queryset = Contrato.objects.filter(formador__usuario = kwargs['initial']['user'])

        self.helper.layout = Layout(
            Fieldset(
                'Selección de contrato',
                Div(
                    Div('contrato',css_class='col-sm-12'),
                    HTML(
                        """
                        <div class="col-sm-12">
                            <div>
                                <p class="inline"><b>Vigencia:</b></p><p class="inline" id="p_vigencia"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Municipios:</b></p><p class="inline" id="p_municipios"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Supervisores:</b></p><p class="inline" id="p_supervisores"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Meta de beneficiarios:</b></p><p class="inline" id="p_meta_beneficiarios"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Inscritos en contrato:</b></p><p class="inline" id="p_inscritos_contrato"> ---- </p>
                            </div>
                            <div>
                                <p class="inline"><b>Inscritos en grupo:</b></p><p class="inline" id="p_inscritos_grupo"> ---- </p>
                            </div>
                        </div>
                        """
                    ),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Información del grupo',
                Div(
                    Div('nombre',css_class='col-sm-6'),
                    Div('diplomado_grupo',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('descripcion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                Div(
                    'numero',css_class='hidden'
                ),
                Div(
                    'usuario',css_class='hidden'
                ),
            )
        )

    class Meta:
        model = GruposBeneficiarios
        fields = '__all__'
        labels = {
            'diplomado_grupo': 'Diplomado',
            'descripcion': 'Descripción',
        }
        widgets = {
            'descripcion': forms.Textarea(),
        }


class BeneficiarioVigenciaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BeneficiarioVigenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        grupo = kwargs['initial']['grupo']

        self.fields['grupo'].initial = grupo
        self.fields['radicado'].queryset = Radicado.objects.filter(municipio__in = grupo.contrato.municipios.all())

        self.helper.layout = Layout(
            Fieldset(
                'Información personal',
                Div(
                    Div('cedula',css_class='col-sm-4'),
                    Div('nombres',css_class='col-sm-4'),
                    Div('apellidos', css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('correo', css_class='col-sm-4'),
                    Div('telefono_fijo', css_class='col-sm-4'),
                    Div('telefono_celular', css_class='col-sm-4'),
                    css_class='row'
                )
            ),
            Fieldset(
                'Institución educativa',
                Div(
                    Div('radicado', css_class='col-sm-12'),
                    css_class='row'
                )
            ),
            Fieldset(
                'Información general',
                Div(
                    Div('area', css_class='col-sm-3'),
                    Div('grado', css_class='col-sm-3'),
                    Div('genero', css_class='col-sm-3'),
                    Div('estado', css_class='col-sm-3'),
                    css_class='row'
                ),
                Div(
                    Div('grupo', css_class='col-sm-6'),
                    css_class='hidden'
                )
            )
        )

    class Meta:
        model = BeneficiarioVigencia
        fields = '__all__'
        labels = {
        }
        widgets = {
            'area' : forms.Select(choices=[
                ('','---------'),
                ('1', 'Ciencias naturales y educación ambiental'),
                ('2', 'Ciencias sociales, historia, geografia, constitución política y/o democrática'),
                ('3', 'Educación artística'),
                ('4', 'Educación ética y en valores humanos'),
                ('5', 'Educación física, recreación y deportes'),
                ('6', 'Educación religiosa'),
                ('7', 'Humanidades'),
                ('8', 'Matemáticas'),
                ('9', 'Lengua castellana'),
                ('10', 'Lengua extranjera: Inglés'),
                ('11', 'Lengua nativa'),
                ('12', 'Competencias ciudadanas'),
                ('13', 'Filosofia'),
                ('14', 'Todas las áreas'),
            ]),

            'grado': forms.Select(choices=[
                ('', '---------'),
                ('0', '0°'),
                ('1', '1°'),
                ('2', '2°'),
                ('3', '3°'),
                ('4', '4°'),
                ('5', '5°'),
                ('6', '6°'),
                ('7', '7°'),
                ('8', '8°'),
                ('9', '9°'),
                ('10', '10°'),
                ('11', '11°'),
                ('12', 'Básica'),
                ('13', 'Media'),
                ('14', 'Modelos educativos flexibles'),
                ('15', 'Todos los grados'),
            ]),

            'genero': forms.Select(choices=[
                ('', '---------'),
                ('F', 'Femenino'),
                ('M', 'Masculino'),
            ]),

            'estado': forms.Select(choices=[
                ('Activo', 'Activo'),
                ('Inactivo', 'Inactivo'),
            ]),
        }