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
from encuestas.models import PercepcionInicial

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
                <button type="submit" class="btn btn-cpe">Responder encuesta</button>
                """)
            ),
        )

    cedula = forms.IntegerField(label='Cedula')

class PercepcionInicialForm(forms.Form):

    def clean(self):
        cleaned_data = super(PercepcionInicialForm, self).clean()
        area = cleaned_data.get('area')
        area_1 = cleaned_data.get('area_1')
        antiguedad = cleaned_data.get('antiguedad')
        pregunta_1 = cleaned_data.get('pregunta_1')
        pregunta_1_1 = cleaned_data.get('pregunta_1_1')
        pregunta_2 = cleaned_data.get('pregunta_2')
        pregunta_3 = cleaned_data.get('pregunta_3')
        pregunta_4 = cleaned_data.get('pregunta_4')
        pregunta_5 = cleaned_data.get('pregunta_5')
        pregunta_6 = cleaned_data.get('pregunta_6')
        pregunta_6_1 = cleaned_data.get('pregunta_6_1')
        pregunta_7 = cleaned_data.get('pregunta_7')
        pregunta_8 = cleaned_data.get('pregunta_8')
        pregunta_9 = cleaned_data.get('pregunta_9')
        pregunta_10 = cleaned_data.get('pregunta_10')
        pregunta_11 = cleaned_data.get('pregunta_11')
        pregunta_12 = cleaned_data.get('pregunta_12')
        pregunta_12_1 = cleaned_data.get('pregunta_12_1')
        pregunta_13 = cleaned_data.get('pregunta_13')

        if area == "15" and area_1 == '':
            self.add_error('area_1','Escribe el area en que te desempeñas')

        if pregunta_1 == "Si":
            if pregunta_2 == "":
                self.add_error('pregunta_2','Debes responder a esta pregunta')

            if pregunta_3 == "":
                self.add_error('pregunta_3','Debes responder a esta pregunta')

            if pregunta_4 == "":
                self.add_error('pregunta_4','Debes responder a esta pregunta')

            if pregunta_5 == "":
                self.add_error('pregunta_5','Debes responder a esta pregunta')

            if pregunta_6 == "":
                self.add_error('pregunta_6','Debes responder a esta pregunta')

            if pregunta_6 == "4" and pregunta_6_1 == '':
                self.add_error('pregunta_6_1','Escribe un beneficio')

            if pregunta_7 == "":
                self.add_error('pregunta_7','Debes responder a esta pregunta')

            if pregunta_12 == "":
                self.add_error('pregunta_12','Debes responder a esta pregunta')

            if pregunta_13 == "":
                self.add_error('pregunta_13','Debes responder a esta pregunta')




            if pregunta_7 == "Si":
                if pregunta_8 == "":
                    self.add_error('pregunta_8','Este campo es requerido')
                if pregunta_9 == "":
                    self.add_error('pregunta_9','Este campo es requerido')
                if pregunta_10 == "":
                    self.add_error('pregunta_10','Este campo es requerido')
                if pregunta_11 == "":
                    self.add_error('pregunta_11','Este campo es requerido')

    #1
    area = forms.CharField(label='',max_length=100,widget=forms.Select(choices=(
        ('','------------------'),
        ('1','Ciencias naturales y educación ambiental'),
        ('2','Ciencias sociales, historia, geografia, constitución politica y/o democrática'),
        ('3','Educación artística'),
        ('4','Educación ética y en valores humanos'),
        ('5','Educación física, recreación y deportes'),
        ('6','Educación religiosa'),
        ('7','Humanidades'),
        ('8','Matemáticas'),
        ('9','Lengua castellana'),
        ('10','Lengua extranjera'),
        ('11','Lengua nativa'),
        ('12','Competencias ciudadanas'),
        ('13','Filosofia'),
        ('14','Todas las áreas'),
        ('15','Otras'),
    )))

    area_1 = forms.CharField(required=False,label='',max_length=100)

    #2
    antiguedad = forms.CharField(label='',max_length=100)
    #3
    pregunta_1 = forms.ChoiceField(label='',
                                 widget=forms.RadioSelect(),choices=(('Si','Si'),('No','No')))
    pregunta_1_1 = forms.CharField(required=False,label="",
                                   max_length=1000,widget=forms.Textarea())
    #4
    pregunta_2 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Formación en herramientas del dispositivo'),
        ('2','b. Formación en contenidos para uso didáctico'),
        ('3','c. Formación en uso avanzado (Programación)'),
        ('4','d. Formación en uso administrativo')
    ))
    #5
    pregunta_3 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Los usas para algunos contenidos (Uso inferior a 4 h semanales)'),
        ('2','b. Los usas para la mayoría los contenidos (Uso entre 4h a 8h semanales)'),
        ('3','c. Los usas de manera intensiva'),
        ('4','d. No usas los dispositivos')
    ))
    #6
    pregunta_4 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Estudio autónomo dentro de la clase de los alumnos'),
        ('2','b. Estudio guiado (clase magistral más trabajo con dispositivos)'),
        ('3','c. Trabajo libre'),
        ('4','d. Trabajo lúdico'),
        ('5','e. Otros'),
    ))
    #7
    pregunta_5 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Sirve como evidencia para ser presentada en el proceso de evaluación de docentes y directivos docentes '),
        ('2','b. Facilita el fortalecimiento de la gestión institucional'),
        ('3','c. Es una herramienta para buscar apoyo académico y técnico a los proyectos de los docentes'),
        ('4','d. Es una herramienta para mejorar la toma de decisiones, articulada a objetivos claros de la institución para el mejoramiento de la calidad'),
    ))
    #8
    pregunta_6 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Ascender en el escalafón docente'),
        ('2','b. Fortalecer tus aprendizajes en el uso pedagógico de las TIC'),
        ('3','c. Conocer contenidos y herramientas que mejoren tus prácticas de enseñanza o de gestión'),
        ('4','d. Otro ¿Cuál?'),
    ))

    pregunta_6_1 = forms.CharField(required=False,label="",max_length=1000,widget=forms.Textarea())
    #9
    pregunta_7 = forms.ChoiceField(required=False,label='',
                                 widget=forms.RadioSelect(),choices=(('Si','Si'),('No','No')))
    #10
    pregunta_8 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Proyectos didácticos (Una sola disciplina)'),
        ('2','b. Proyectos productivos (Una sola disciplina)'),
        ('3','c. Proyectos de articulación con otras disciplinas'),
        ('4','d. Otros proyectos no clasificados'),
    ))
    #11
    pregunta_9 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Sirven como evidencia para la evaluación docente'),
        ('2','b. Permiten participar en eventos nacionales o internacionales'),
        ('3','c. Facilitan los aprendizajes de los estudiantes y las prácticas de enseñanza del docente'),
        ('4','d. Son una oportunidad para seguir cualificando la práctica docente'),
    ))
    #12
    pregunta_10 = forms.ChoiceField(required=False,label='',
                                 widget=forms.RadioSelect(),choices=(('Si','Si'),('No','No')))
    #13
    pregunta_11 = forms.ChoiceField(required=False,label="",widget=forms.RadioSelect(),choices=(
        ('1','a. 1-2 Horas semanales'),
        ('2','b. 2-6 Horas semanales'),
        ('3','c. 6 o más horas semanales'),
        ('4','d. No dedicaría tiempo adicional'),
    ))
    #14
    pregunta_12 = forms.ChoiceField(required=False,label='',
                                 widget=forms.RadioSelect(),choices=(('Si','Si'),('No','No')))

    pregunta_12_1 = forms.CharField(required=False,label="",max_length=1000,widget=forms.Textarea())

    #15
    pregunta_13 = forms.CharField(required=False,label="",max_length=100)

    def __init__(self,*args, **kwargs):
        super(PercepcionInicialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '1. ¿En que área te desempeñas como docente?',
                Div(
                    Div('area',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '¿Cual?',
                Div(
                    Div('area_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_id="otra_area",
                css_class='fieldset_class hidden'
            ),
            Fieldset(
                '2. ¿Cuantos años de experiencia tienes en docencia?',
                Div(
                    Div('antiguedad',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '3. ¿Te gustaría recibir capacitación especializada sobre TIC y Educación relacionada con el uso de '
                'contenidos para aprender?',
                Div(
                    Div('pregunta_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '¿Nos dirias por qué?',
                Div(
                    Div('pregunta_1_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class='fieldset_class hidden',
                css_id='fieldset_pregunta_1_1'
            ),
            Div(
                Fieldset(
                    '4. ¿Cuál de los siguientes contenidos y utilidades te parece más relevante en la formación?',
                    Div(
                        Div('pregunta_2',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '5. ¿Qué uso le das a los dispositivos en tu colegio actualmente?',
                    Div(
                        Div('pregunta_3',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '6. ¿Respecto a la pregunta anterior cuales son los usos más frecuentes que le das a los dispositivos?',
                    Div(
                        Div('pregunta_4',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '7. ¿Cuál es tu motivación principal para recibir la capacitación?',
                    Div(
                        Div('pregunta_5',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '8. ¿Cuál de los siguientes beneficios consideras es el más importante para ti al recibir una charla o participar en un curso o diplomado en TIC y educación?',
                    Div(
                        Div('pregunta_6',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    Div(
                        Div('pregunta_6_1',css_class='col-sm-12'),
                        css_class = 'row hidden',
                        css_id='otro_1'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '9. ¿Si recibes el curso estarías dispuesto a aplicar tus conocimientos en un proyecto pedagógico con resultados reales articulado con las TIC?',
                    Div(
                        Div('pregunta_7',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                css_class = 'hidden',
                css_id='primer_condicional'
            ),
            Div(
                Fieldset(
                    '10. ¿En qué área aplicarías los conocimientos?',
                    Div(
                        Div('pregunta_8',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '11. ¿Cuál de las siguientes razones justificaría tu interés por desarrollar proyectos pedagógicos que articulen las TIC?',
                    Div(
                        Div('pregunta_9',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '12. ¿Consideras que se pueden solucionar problemas que se presentan en el proceso de enseñanza – aprendizaje con tus estudiantes a través del uso de las TIC?',
                    Div(
                        Div('pregunta_10',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '13. ¿Cuál es el rango de tiempo que le dedicarías a practicar lo aprendido?',
                    Div(
                        Div('pregunta_11',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                css_class = 'hidden',
                css_id='segundo_condicional'
            ),
            Div(
                Fieldset(
                    '14. ¿Has participado en procesos de formación (seminarios, diplomados u otros cursos) sobre el uso de computadores o tabletas, programados por Computadores para Educar o por otros programas o iniciativas?',
                    Div(
                        Div('pregunta_12',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    Div(
                        Div(
                            Fieldset(
                                'Cuéntanos tu experiencia, ¿Que le mejorarías?',
                                Div(
                                    Div('pregunta_12_1',css_class='col-sm-12'),
                                    css_class = 'row'
                                )
                            ),
                        ),
                        css_class = 'row hidden',
                        css_id='otro_2'
                    ),
                    css_class="fieldset_class"
                ),
                Fieldset(
                    '15. ¿En una escala de 0% a 100% que porcentaje de conocimiento consideras que tienes actualmente en el uso de las TIC?',
                    Div(
                        Div('pregunta_13',css_class='col-sm-12'),
                        css_class = 'row'
                    ),
                    css_class="fieldset_class"
                ),
                css_class = 'hidden fieldset_class',
                css_id='tercer_condicional'
            ),
            HTML(
                """
                <button type="submit" class="btn btn-cpe">Enviar respuestas</button>
                """
            )
        )

class PercepcionFinalForm(forms.Form):
    #1
    area = forms.CharField(label='',max_length=100,widget=forms.Select(choices=(
        ('','------------------'),
        ('1','Ciencias naturales y educación ambiental'),
        ('2','Ciencias sociales, historia, geografia, constitución politica y/o democrática'),
        ('3','Educación artística'),
        ('4','Educación ética y en valores humanos'),
        ('5','Educación física, recreación y deportes'),
        ('6','Educación religiosa'),
        ('7','Humanidades'),
        ('8','Matemáticas'),
        ('9','Lengua castellana'),
        ('10','Lengua extranjera'),
        ('11','Lengua nativa'),
        ('12','Competencias ciudadanas'),
        ('13','Filosofia'),
        ('14','Todas las áreas'),
        ('15','Otras'),
    )))


    #2
    tiempo_formacion = forms.CharField(label='',max_length=100)
    #3
    pregunta_1 = forms.CharField(label='',max_length=100)
    #4
    pregunta_2 = forms.CharField(label='',max_length=100)
    #5
    pregunta_3 = forms.CharField(label='',max_length=100)
    #6
    pregunta_4 = forms.CharField(label='',max_length=100)
    #7
    pregunta_5 = forms.CharField(label='',max_length=100)

    #8
    pregunta_6 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))

    pregunta_7 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))

    pregunta_8 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))

    pregunta_9 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))

    pregunta_10 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))

    pregunta_11 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))

    pregunta_12 = forms.ChoiceField(label="",widget=forms.RadioSelect(),choices=(
        ('1','a. Totalmente en desacuerdo'),
        ('2','b. En desacuerdo'),
        ('3','c. Neutral (Ni en desacuerdo ni de acuerdo)'),
        ('4','d. De acuerdo'),
        ('5','e. Totalmente de acuerdo'),
    ))


    def __init__(self,*args, **kwargs):
        super(PercepcionFinalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '1. ¿En que área te desempeñas como docente?',
                Div(
                    Div('area',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '2. ¿Cuanto tiempo llevas en formación?',
                Div(
                    Div('tiempo_formacion',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '3. ¿Cuál fue el grado de terminación de contenidos respecto del contenido inicial?',
                Div(
                    Div('pregunta_1',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '4. ¿Cuántas horas se dedicaron en total de manera presencial al curso?',
                Div(
                    Div('pregunta_2',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '5. ¿Cuántas horas se dedicaron en total de manera virtual al curso?',
                Div(
                    Div('pregunta_3',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '6. ¿Cuál fue la dedicación del formador en horas extras al seguimiento y colaboración?',
                Div(
                    Div('pregunta_4',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '7. ¿Cuál fue el porcentaje de avance del proyecto pedagógico?',
                Div(
                    Div('pregunta_5',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '8. ¿El formador transmitió los conceptos adecuadamente?',
                Div(
                    Div('pregunta_6',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '9. ¿El formador cumplió con los tiempos y horarios establecidos y planeados?',
                Div(
                    Div('pregunta_7',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '10. ¿El formador dedicó tiempo a la guianza personalizada de las sesiones?',
                Div(
                    Div('pregunta_8',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '11. ¿El formador presentó los temas con la suficiencia y conocimiento requerido para hacerse entender?',
                Div(
                    Div('pregunta_9',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '12. ¿El formador respondió a sus preguntas y consultas oportunamente (dentro de los tres días siguientes al envío de la consulta)?',
                Div(
                    Div('pregunta_10',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '13. ¿Los contenidos vistos llenaron sus expectativas?',
                Div(
                    Div('pregunta_11',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),
            Fieldset(
                '14. ¿Los contenidos vistos han sido de utilidad en el desarrollo de la actividad de clase?',
                Div(
                    Div('pregunta_12',css_class='col-sm-12'),
                    css_class = 'row'
                ),
                css_class="fieldset_class"
            ),

            HTML(
                """
                <button type="submit" class="btn btn-cpe">Enviar respuestas</button>
                """
            )
        )