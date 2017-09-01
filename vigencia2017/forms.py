#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from radicados.models import Radicado, RadicadoRetoma
from secretarias.models import Secretaria
from municipios.models import Municipio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML, Button
from vigencia2017.models import DaneSEDE, Grupos, TipoContrato, ValorEntregableVigencia2017, CargaMatriz, Beneficiario
from formadores.models import Contrato
from productos.models import Entregable
from usuarios.models import User
import openpyxl
from region.models import Region
from vigencia2017.models import Evidencia, Red


class DaneSEDEForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DaneSEDEForm, self).__init__(*args, **kwargs)
        self.fields['secretaria'].queryset = Secretaria.objects.exclude(oculto = True)
        self.fields['municipio'].queryset = Municipio.objects.exclude(oculto = True)
        self.fields['zona'].widget = forms.Select(choices = [('','----------'),('RURAL','RURAL'),('URBANA','URBANA')])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información Sede',
                Div(
                    Div('municipio', css_class='col-sm-6'),
                    Div('secretaria', css_class='col-sm-6'),
                    css_class='row'
                ),
                Div(
                    Div('dane_sede',css_class='col-sm-4'),
                    Div('nombre_sede',css_class='col-sm-4'),
                    Div('zona', css_class='col-sm-4'),
                    css_class = 'row'
                )
            ),
            Fieldset(
                'Institución Educativa',
                Div(
                    Div('dane_ie', css_class='col-sm-6'),
                    Div('nombre_ie', css_class='col-sm-6'),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = DaneSEDE
        fields = '__all__'
        labels = {
        }

class GruposForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GruposForm, self).__init__(*args, **kwargs)
        self.fields['contrato'].initial = Contrato.objects.get(id = kwargs['initial']['id_contrato'])
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información Grupo',
                Div(
                    Div('diplomado', css_class='col-sm-6'),
                    Div('numero', css_class='col-sm-6'),
                    css_class='row'
                ),
                Div(
                    Div('archivo', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('contrato', css_class='hidden'),
                    css_class='row'
                )
            ),
        )

    class Meta:
        model = Grupos
        fields = '__all__'
        labels = {
        }

class GruposVigencia2017ConectividadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GruposVigencia2017ConectividadForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Certificado de no conectividad',
                Div(
                    Div('archivo', css_class='col-sm-12'),
                    css_class='row'
                )
            ),
        )

    class Meta:
        model = Grupos
        fields = ['archivo']
        labels = {
        }

class TipoContratoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TipoContratoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información del contrato',
                Div(
                    Div('nombre', css_class='col-sm-12'),
                    css_class='row'
                ),
                Div(
                    Div('diplomados', css_class='col-sm-12'),
                    css_class='row'
                )
            )
        )

    class Meta:
        model = TipoContrato
        exclude = ['entregables']
        labels = {
        }

class ValorEntregableVigencia2017Form(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ValorEntregableVigencia2017Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        entregables = Entregable.objects.filter(sesion__nivel__diplomado__id=kwargs['initial']['id_diplomado']).order_by('numero')
        tipo_contrato = TipoContrato.objects.get(id=kwargs['initial']['id_contrato'])

        nivel_count = 0
        data = {}
        field_count = 0

        for entregable in entregables:
            nombre_nivel = entregable.sesion.nivel.nombre
            nombre_sesion = entregable.sesion.nombre

            if nombre_nivel not in data.keys():
                self.helper.layout.fields.append(Fieldset(nombre_nivel))
                data[nombre_nivel] = {'position':nivel_count,'sesiones':{},'count':0}
                nivel_count += 1


            if nombre_sesion not in data[nombre_nivel]['sesiones'].keys():
                self.helper.layout.fields[ data[nombre_nivel]['position'] ].append(Fieldset("N"+str(data[nombre_nivel]['position'])+": "+nombre_sesion))
                data[nombre_nivel]['sesiones'][nombre_sesion] = {'position': data[nombre_nivel]['count']}
                data[nombre_nivel]['count'] += 1

            self.fields[str(entregable.id)] = forms.FloatField(label=str(entregable.numero)+" - "+entregable.nombre,initial=0)
            self.helper.layout.fields[data[nombre_nivel]['position']].fields[data[nombre_nivel]['sesiones'][nombre_sesion]['position']].append(Div(str(entregable.id)))


            try:
                valor = ValorEntregableVigencia2017.objects.get(entregable=entregable, tipo_contrato=tipo_contrato)
            except:
                pass
            else:
                self.fields[str(entregable.id)].initial = valor.valor

class CargaMatrizForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data

        wb = openpyxl.load_workbook(self.cleaned_data['archivo'])
        sheet_names = wb.get_sheet_names()

        if u'InnovaTIC' in sheet_names and u'TecnoTIC' in sheet_names and u'DirecTIC' in sheet_names:
            pass

        elif u'Matriz revisión documental' in sheet_names:
            pass

        else:
            self._errors['archivo'] = self.error_class(u'El archivo no tiene la estructura necesaria')

        return data

    def __init__(self, *args, **kwargs):
        super(CargaMatrizForm, self).__init__(*args, **kwargs)

        self.fields['usuario'].initial = User.objects.get(id = kwargs['initial']['id_usuario'])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Matriz',
                Div(
                    Div('usuario', css_class='hidden'),
                    css_class='row'
                ),
                Div(
                    Div('archivo', css_class='col-sm-12'),
                    css_class='row'
                )
            )
        )


    class Meta:
        model = CargaMatriz
        fields = "__all__"
        labels = {
        }

class BeneficiarioVigencia2017Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BeneficiarioVigencia2017Form, self).__init__(*args, **kwargs)

        contrato = Contrato.objects.get(id=kwargs['initial']['id_contrato'])
        grupo = Grupos.objects.get(id=kwargs['initial']['id_grupo'])

        if grupo.diplomado.id in [1,2,3]:
            self.fields['dane_sede'].required = True
            self.fields['area'].required = True
            self.fields['grado'].required = True
            self.fields['genero'].required = True

            self.fields['grupo'].queryset = Grupos.objects.filter(contrato = contrato)
            self.fields['dane_sede'].queryset = DaneSEDE.objects.filter(municipio__id__in = contrato.municipios.all().values_list('id',flat=True))

            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Fieldset(
                    'Información Personal',
                    Div(
                        Div('nombres', css_class='col-sm-3'),
                        Div('apellidos', css_class='col-sm-3'),
                        Div('cedula', css_class='col-sm-3'),
                        Div('grupo', css_class='col-sm-3'),
                        css_class='row'
                    ),
                    Div(
                        Div('correo', css_class='col-sm-3'),
                        Div('telefono_fijo', css_class='col-sm-3'),
                        Div('telefono_celular', css_class='col-sm-3'),
                        Div('genero', css_class='col-sm-3'),
                        css_class='row'
                    ),
                ),
                Fieldset(
                    'Información laboral',
                    Div(
                        Div('dane_sede', css_class='col-sm-8'),
                        Div('area', css_class='col-sm-2'),
                        Div('grado', css_class='col-sm-2'),
                        css_class='row'
                    )
                )
            )
        else:
            self.fields['genero'].required = True
            self.fields['municipio'].required = True

            self.fields['grupo'].queryset = Grupos.objects.filter(contrato=contrato)
            self.fields['municipio'].queryset = Municipio.objects.filter(id__in = contrato.municipios.all().values_list('id',flat=True))

            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Fieldset(
                    'Información Personal',
                    Div(
                        Div('nombres', css_class='col-sm-2'),
                        Div('apellidos', css_class='col-sm-2'),
                        Div('cedula', css_class='col-sm-2'),
                        Div('grupo', css_class='col-sm-3'),
                        Div('municipio', css_class='col-sm-3'),
                        css_class='row'
                    ),
                    Div(
                        Div('correo', css_class='col-sm-3'),
                        Div('telefono_fijo', css_class='col-sm-3'),
                        Div('telefono_celular', css_class='col-sm-3'),
                        Div('genero', css_class='col-sm-3'),
                        css_class='row'
                    ),
                    Div(
                        Div('area', css_class='col-sm-3'),
                        Div('grado', css_class='col-sm-3'),
                        Div('dane_sede', css_class='col-sm-3'),
                        Div('region', css_class='col-sm-3'),
                        css_class='hidden'
                    )
                )
            )

    class Meta:
        model = Beneficiario
        exclude = ['region']
        labels = {
        }
        widgets = {
            'genero': forms.Select(choices=[('', '----------'), ('FEMENINO', 'FEMENINO'), ('MASCULINO', 'MASCULINO')]),
            'area': forms.Select(
                choices=[('', '----------'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                         ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                         ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15')]),
            'grado': forms.Select(
                choices=[('', '----------'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                         ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                         ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15')]),
        }

class NewBeneficiarioVigencia2017Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewBeneficiarioVigencia2017Form, self).__init__(*args, **kwargs)

        contrato = Contrato.objects.get(id=kwargs['initial']['id_contrato'])
        grupo = Grupos.objects.get(id=kwargs['initial']['id_grupo'])
        departamentos = contrato.municipios.values_list('departamento',flat=True)
        region = Region.objects.filter(departamentos__id__in = departamentos)

        self.fields['grupo'].queryset = Grupos.objects.filter(contrato = contrato)
        self.fields['grupo'].initial = Grupos.objects.filter(contrato = contrato).get(id = kwargs['initial']['id_grupo'])
        self.fields['dane_sede'].queryset = DaneSEDE.objects.filter(municipio__id__in = contrato.municipios.all().values_list('id',flat=True))
        self.fields['region'].initial = region[0]
        if grupo.diplomado.id in [1,2,3]:
            self.fields['dane_sede'].required = True
            self.fields['area'].required = True
            self.fields['grado'].required = True
            self.fields['genero'].required = True

            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Fieldset(
                    'Información Personal',
                    Div(
                        Div('nombres', css_class='col-sm-4'),
                        Div('apellidos', css_class='col-sm-4'),
                        Div('cedula', css_class='col-sm-4'),
                        css_class='row'
                    ),
                    Div(
                        Div('grupo', css_class='hidden'),
                        Div('region', css_class='hidden'),
                        css_class='row'
                    ),
                    Div(
                        Div('correo', css_class='col-sm-3'),
                        Div('telefono_fijo', css_class='col-sm-3'),
                        Div('telefono_celular', css_class='col-sm-3'),
                        Div('genero', css_class='col-sm-3'),
                        css_class='row'
                    ),
                ),
                Fieldset(
                    'Información laboral',
                    Div(
                        Div('dane_sede', css_class='col-sm-8'),
                        Div('area', css_class='col-sm-2'),
                        Div('grado', css_class='col-sm-2'),
                        css_class='row'
                    )
                )
            )
        else:
            self.fields['genero'].required = True
            self.fields['municipio'].required = True
            self.fields['area'].required = False
            self.fields['grado'].required = False

            self.fields['grupo'].queryset = Grupos.objects.filter(contrato=contrato)
            self.fields['municipio'].queryset = Municipio.objects.filter(id__in = contrato.municipios.all().values_list('id',flat=True))

            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Fieldset(
                    'Información Personal',
                    Div(
                        Div('nombres', css_class='col-sm-3'),
                        Div('apellidos', css_class='col-sm-3'),
                        Div('cedula', css_class='col-sm-3'),
                        Div('municipio', css_class='col-sm-3'),

                        css_class='row'
                    ),
                    Div(
                        Div('correo', css_class='col-sm-3'),
                        Div('telefono_fijo', css_class='col-sm-3'),
                        Div('telefono_celular', css_class='col-sm-3'),
                        Div('genero', css_class='col-sm-3'),
                        css_class='row'
                    ),
                    Div(
                        Div('grupo', css_class='col-sm-3'),
                        Div('area', css_class='col-sm-3'),
                        Div('grado', css_class='col-sm-3'),
                        Div('dane_sede', css_class='col-sm-3'),
                        Div('region', css_class='col-sm-3'),
                        css_class='hidden'
                    )
                )
            )

    class Meta:
        model = Beneficiario
        fields = '__all__'
        labels = {
        }
        widgets = {
            'genero': forms.Select(choices=[('','----------'),('FEMENINO','FEMENINO'),('MASCULINO','MASCULINO')]),
            'area': forms.Select(choices=[('', '----------'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                                          ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),('11', '11'),
                                          ('12', '12'), ('13', '13'), ('14', '14')]),
            'grado': forms.Select(
                choices=[('', '----------'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                         ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'),
                         ('12', '12'), ('13', '13'), ('14', '14')]),
        }

class EvidenciaVigencia2017Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EvidenciaVigencia2017Form, self).__init__(*args, **kwargs)

        contrato = Contrato.objects.get(id=kwargs['initial']['id_contrato'])
        entregable = Grupos.objects.get(id=kwargs['initial']['id_grupo'])
        entregable = Entregable.objects.get(id=kwargs['initial']['id_entregable'])
        grupo = Grupos.objects.get(id=kwargs['initial']['id_grupo'])

        self.fields['contrato'].initial = contrato
        self.fields['entregable'].initial = entregable
        self.fields['usuario'].initial = User.objects.get(id=kwargs['initial']['id_usuario'])

        queryset = Beneficiario.objects.filter(grupo__contrato = contrato)
        evidencias = Evidencia.objects.filter(contrato = contrato,entregable = entregable)
        #reds = Red.objects.filter(evidencias__id__in = evidencias.values_list('id',flat=True))

        exclude_validados = list(evidencias.exclude(beneficiarios_validados = None).values_list('beneficiarios_validados__id',flat=True))

        exclude_enviados = []

        for red_id in evidencias.values_list('red_id',flat=True).distinct():
            try:
                red = Red.objects.get(id = red_id)
            except:
                pass
            else:
                if not red.retroalimentacion:
                    for evidencia in evidencias.filter(red_id = red_id):
                        for cargado in evidencia.beneficiarios_cargados.all():
                            exclude_enviados.append(cargado.id)

            #for evidencia in evidencias.filter(id__in = reds.filter(retroalimentacion = False).values_list('evidencias__id',flat=True)):
            #    for cargado in evidencia.beneficiarios_cargados.all():
            #        exclude_enviados.append(cargado.id)


        self.fields['beneficiarios_cargados'].queryset = queryset.exclude(id__in = exclude_validados + exclude_enviados)


        if entregable.escencial == "No":

            self.fields.pop('archivo')
            self.fields['link'] = forms.URLField(max_length=200)

            self.helper = FormHelper(self)
            self.helper.layout = Layout(
                Fieldset(
                    'Evidencia',
                    Div(
                        Div('link', css_class='col-sm-12'),
                        css_class='row'
                    ),
                    Div(
                        Div(
                            Button('set_grupo', "Cargar grupo de beneficiarios", css_class='btn'),
                            css_class='col-sm-12'
                        ),
                        css_class='row'
                    ),
                    Div(
                        HTML('''</br>'''),
                        css_class='row'
                    ),
                    Div(
                        Div('beneficiarios_cargados', css_class='col-sm-12'),
                        css_class='row'
                    ),
                    Div(
                        Div('usuario', css_class='col-sm-12'),
                        css_class='hidden'
                    ),
                    Div(
                        Div('entregable', css_class='col-sm-12'),
                        css_class='hidden'
                    ),
                    Div(
                        Div('contrato', css_class='col-sm-12'),
                        css_class='hidden'
                    )
                ),
                Fieldset(
                    'Excel',
                    Div(
                        Div('masivos', css_class='col-sm-12'),
                        css_class='row'
                    )
                ),
            )

        elif entregable.escencial == "Si":

            if grupo.no_conectividad == False and entregable.tipo == "Virtual":
                self.fields.pop('archivo')
                self.fields['link'] = forms.URLField(max_length=200)

                self.helper = FormHelper(self)
                self.helper.layout = Layout(
                    Fieldset(
                        'Evidencia',
                        Div(
                            Div('link', css_class='col-sm-12'),
                            css_class='row'
                        ),
                        Div(
                            Div(
                                Button('set_grupo', "Cargar grupo de beneficiarios", css_class='btn'),
                                css_class='col-sm-12'
                            ),
                            css_class='row'
                        ),
                        Div(
                            HTML('''</br>'''),
                            css_class='row'
                        ),
                        Div(
                            Div('beneficiarios_cargados', css_class='col-sm-12'),
                            css_class='row'
                        ),
                        Div(
                            Div('usuario', css_class='col-sm-12'),
                            css_class='hidden'
                        ),
                        Div(
                            Div('entregable', css_class='col-sm-12'),
                            css_class='hidden'
                        ),
                        Div(
                            Div('contrato', css_class='col-sm-12'),
                            css_class='hidden'
                        )
                    ),
                    Fieldset(
                        'Excel',
                        Div(
                            Div('masivos', css_class='col-sm-12'),
                            css_class='row'
                        )
                    ),
                )

            else:
                self.helper = FormHelper(self)
                self.helper.layout = Layout(
                    Fieldset(
                        'Evidencia',
                        Div(
                            Div('archivo',css_class='col-sm-12'),
                            css_class = 'row'
                        ),
                        Div(
                            Div(
                                Button('set_grupo', "Cargar grupo de beneficiarios", css_class='btn'),
                                css_class='col-sm-12'
                            ),
                            css_class='row'
                        ),
                        Div(
                            HTML('''</br>'''),
                            css_class='row'
                        ),
                        Div(
                            Div('beneficiarios_cargados',css_class='col-sm-12'),
                            css_class = 'row'
                        ),
                        Div(
                            Div('usuario',css_class='col-sm-12'),
                            css_class = 'hidden'
                        ),
                        Div(
                            Div('entregable',css_class='col-sm-12'),
                            css_class = 'hidden'
                        ),
                        Div(
                            Div('contrato',css_class='col-sm-12'),
                            css_class = 'hidden'
                        )
                    ),
                    Fieldset(
                        'Excel',
                        Div(
                            Div('masivos',css_class='col-sm-12'),
                            css_class = 'row'
                        )
                    ),
                )


    masivos = forms.CharField(max_length=1000,required=False,label='Cedulas',widget=forms.Textarea())

    class Meta:
        model = Evidencia
        fields = ['usuario','archivo','entregable','beneficiarios_cargados','contrato']

class MasivoVigencia2017Form(forms.Form):
    archivo = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/zip'}))

    def __init__(self, *args, **kwargs):
        super(MasivoVigencia2017Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Carga masiva de evidencias',
                Div(
                    Div('archivo', css_class='col-sm-12'),
                    css_class='row'
                )
            )
        )

class RedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RedForm, self).__init__(*args, **kwargs)

        self.fields['region'].queryset = Region.objects.exclude(numero__in = [4,3])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Información R1',
                Div(
                    HTML(
                        """
                        <div class="row">
                            <div class="col-sm-3">
                                <h4 class="bold-p" style="margin-bottom:10px;">Innovatic</h4>
                                <p>Formadores: {{formadores_innovatic_r1}}</p>
                                <p>Beneficiarios: {{beneficiarios_innovatic_r1}}</p>
                                <p>Evidencias: {{evidencias_innovatic_r1}}</p>
                            </div>
                            <div class="col-sm-3">
                                <h4 class="bold-p">Tecnotic</h4>
                                <p>Formadores: {{formadores_tecnotic_r1}}</p>
                                <p>Beneficiarios: {{beneficiarios_tecnotic_r1}}</p>
                                <p>Evidencias: {{evidencias_tecnotic_r1}}</p>
                            </div>

                            <div class="col-sm-3">
                                <h4 class="bold-p">Directic</h4>
                                <p>Formadores: {{formadores_directic_r1}}</p>
                                <p>Beneficiarios: {{beneficiarios_directic_r1}}</p>
                                <p>Evidencias: {{evidencias_directic_r1}}</p>
                            </div>
                            <div class="col-sm-3">
                                <h4 class="bold-p">Escuela TIC</h4>
                                <p>Formadores: {{formadores_escuelatic_r1}}</p>
                                <p>Beneficiarios: {{beneficiarios_escuelatic_r1}}</p>
                                <p>Evidencias: {{evidencias_escuelatic_r1}}</p>
                            </div>
                        </div>
                        """,
                    ),
                )
            ),
            Fieldset(
                'Información R2',
                Div(
                    HTML(
                        """
                        <div class="row">
                            <div class="col-sm-3">
                                <h4 class="bold-p" style="margin-bottom:10px;">Innovatic</h4>
                                <p>Formadores: {{formadores_innovatic_r2}}</p>
                                <p>Beneficiarios: {{beneficiarios_innovatic_r2}}</p>
                                <p>Evidencias: {{evidencias_innovatic_r2}}</p>
                            </div>
                            <div class="col-sm-3">
                                <h4 class="bold-p">Tecnotic</h4>
                                <p>Formadores: {{formadores_tecnotic_r2}}</p>
                                <p>Beneficiarios: {{beneficiarios_tecnotic_r2}}</p>
                                <p>Evidencias: {{evidencias_tecnotic_r2}}</p>
                            </div>

                            <div class="col-sm-3">
                                <h4 class="bold-p">Directic</h4>
                                <p>Formadores: {{formadores_directic_r2}}</p>
                                <p>Beneficiarios: {{beneficiarios_directic_r2}}</p>
                                <p>Evidencias: {{evidencias_directic_r2}}</p>
                            </div>
                            <div class="col-sm-3">
                                <h4 class="bold-p">Escuela TIC</h4>
                                <p>Formadores: {{formadores_escuelatic_r2}}</p>
                                <p>Beneficiarios: {{beneficiarios_escuelatic_r2}}</p>
                                <p>Evidencias: {{evidencias_escuelatic_r2}}</p>
                            </div>
                        </div>
                        """,
                    ),
                )
            ),
            Fieldset(
                'RED',
                Div(
                    Div('diplomado',css_class='col-sm-6'),
                    Div('region',css_class='col-sm-6'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = Red
        exclude = ['producto_final']