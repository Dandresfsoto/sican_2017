#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from evidencias.models import Evidencia
from formadores.models import Formador
from productos.models import Entregable
from usuarios.models import User
from matrices.models import Beneficiario
from evidencias.models import Red, CargaMasiva
from region.models import Region
from datetime import datetime

class EvidenciaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EvidenciaForm, self).__init__(*args, **kwargs)

        formador = Formador.objects.get(id=kwargs['initial']['id_formador'])
        entregable = Entregable.objects.get(id=kwargs['initial']['id_entregable'])

        self.fields['formador'].initial = formador
        self.fields['entregable'].initial = entregable
        self.fields['usuario'].initial = User.objects.get(id=kwargs['initial']['id_usuario'])

        queryset = Beneficiario.objects.filter(formador__id=kwargs['initial']['id_formador'])
        evidencias = Evidencia.objects.filter(formador = formador,entregable = entregable)
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

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Evidencia',
                Div(
                    Div('archivo',css_class='col-sm-12'),
                    css_class = 'row'
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
                    Div('formador',css_class='col-sm-12'),
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
        fields = ['usuario','archivo','entregable','beneficiarios_cargados','formador']

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
                                <p>PLE: {{ple_r1}}</p>
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
                                <p>PLE: {{ple_r2}}</p>
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
                    Div('diplomado',css_class='col-sm-4'),
                    Div('region',css_class='col-sm-4'),
                    Div('producto_final', css_class='col-sm-4'),
                    css_class = 'row'
                )
            ),
        )
    masivos = forms.CharField(max_length=1000,required=False,label='Cedulas',widget=forms.Textarea())

    class Meta:
        model = Red
        fields = '__all__'

class CargaMasivaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CargaMasivaForm, self).__init__(*args, **kwargs)

        self.fields['usuario'].initial = User.objects.get(id = kwargs['initial']['id_usuario'])
        self.fields['excel'].widget.attrs.update({
            'accept' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        self.fields['zip'].widget.attrs.update({
            'accept' : '.zip'
        })

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'RED',
                Div(
                    Div('excel',css_class='col-sm-6'),
                    Div('zip',css_class='col-sm-6'),
                    css_class = 'row'
                ),
                Div(
                    Div('usuario',css_class='col-sm-6'),
                    css_class = 'hidden'
                )
            ),
        )

    class Meta:
        model = CargaMasiva
        fields = ['excel','zip','usuario']

class RedRetroalimentacionForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(RedRetroalimentacionForm, self).clean()
        archivo_retroalimentacion = cleaned_data.get('archivo_retroalimentacion')

        if archivo_retroalimentacion == None:
            self.add_error('archivo_retroalimentacion','Este campo es requerido.')


    def __init__(self, *args, **kwargs):
        super(RedRetroalimentacionForm, self).__init__(*args, **kwargs)


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'RETROALIMENTACIÓN',
                Div(
                    Div('archivo_retroalimentacion',css_class='col-sm-12'),
                    css_class = 'row'
                )
            ),
        )

    class Meta:
        model = Red
        fields = ['archivo_retroalimentacion']
        labels = {
            'archivo_retroalimentacion': 'Archivo de retroalimentación'
        }

class SubsanacionEvidenciaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SubsanacionEvidenciaForm, self).__init__(*args, **kwargs)

        red = Red.objects.get(id=kwargs['initial']['id_red'])
        evidencia = Evidencia.objects.get(id=kwargs['initial']['id_evidencia'])

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Soporte',
                HTML(
                    """
                    <p>Original: <a target="_blank" href="{{link_soporte}}">{{nombre_soporte}}</a></p>
                    """
                ),
                Div(
                    Div('archivo',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                HTML(
                    """
                    <p>*Solo use este campo si es necesario reemplazar el archivo original.</p>
                    """
                )
            ),
        )

        self.helper.layout.fields.append(Fieldset('Beneficiarios',
                                                  Div(
                                                      Div(
                                                          Div(HTML("""<p style="color:#004c99;font-weight:bold;font-size:18px">Nombre</p>"""),css_class='col-sm-3'),
                                                          Div(HTML("""<p style="color:#004c99;font-weight:bold;font-size:18px">Cedula</p>"""),css_class='col-sm-2'),
                                                          Div(HTML("""<p style="color:#004c99;font-weight:bold;font-size:18px">Grupo</p>"""),css_class='col-sm-2'),
                                                          Div(HTML("""<p style="color:#004c99;font-weight:bold;font-size:18px">Motivo de rechazo</p>"""),css_class='col-sm-3'),
                                                          Div(HTML("""<p style="color:#004c99;font-weight:bold;font-size:18px">Subsanado</p>"""),css_class='col-sm-2'),
                                                          css_class = 'row'),
                                                      css_class = 'container-fluid')
                                                  )
                                         )


        self.helper.layout.fields.append(Fieldset('Observación',
                                                  Div(
                                                      'observacion',
                                                      css_class = 'container-fluid')
                                                  )
                                         )



        container = self.helper.layout.fields[1].fields[0]


        for rechazo in evidencia.beneficiarios_rechazados.all():

            nombre = 'beneficiario_' + str(rechazo.beneficiario_rechazo.id)

            self.fields[nombre] = forms.BooleanField(label="",required=False)

            container.append(Div(
                                    Div(HTML("""<p style="margin-top:10px"><a href='beneficiario/""" + str(rechazo.beneficiario_rechazo.id) + """ '>"""+ rechazo.beneficiario_rechazo.get_full_name() +"""</a></p>"""),css_class='col-sm-3'),
                                    Div(HTML("""<p style="margin-top:10px">"""+ str(rechazo.beneficiario_rechazo.cedula) +"""</p>"""),css_class='col-sm-2'),
                                    Div(HTML("""<p style="margin-top:10px">"""+ rechazo.beneficiario_rechazo.get_grupo() +"""</p>"""),css_class='col-sm-2'),
                                    Div(HTML("""<p style="margin-top:10px">"""+ rechazo.observacion +"""</p>"""),css_class='col-sm-3'),
                                    Div(nombre,css_class='col-sm-2'),
                                    css_class = 'row'
                                )
                            )

        x = 0

    archivo = forms.FileField(required=False)
    observacion = forms.CharField(max_length=100,widget = forms.Textarea(),required=False,label="*Use este campo en caso de requerir un comentario adicional")
