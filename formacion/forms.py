from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, HTML
from formacion.models import EntradaCronograma
from formadores.models import Formador
from formacion.models import Semana
from departamentos.models import Departamento
from municipios.models import Municipio
from secretarias.models import Secretaria
from formadores.models import Grupos
from productos.models import Diplomado, Nivel, Actividades
import datetime

class EntradaCronogramaform(forms.ModelForm):

    def clean(self):
        cleaned_data = super(EntradaCronogramaform, self).clean()
        actividades = cleaned_data.get('actividades_entrada')
        hora_inicio = cleaned_data.get('hora_inicio')
        formador = cleaned_data.get('formador')
        fecha = cleaned_data.get('fecha')


        id_actividades = []
        delta = 0
        if len(actividades) != 0:
            for actividad in actividades:
                id_actividades.append(actividad.id)

            tiempo = Actividades.objects.filter(id__in=id_actividades).values_list('horas',flat=True)
            delta = sum(tiempo)

            if hora_inicio.hour + delta <= 22:

                horas = []
                entradas = EntradaCronograma.objects.filter(formador=formador,fecha=fecha)

                for entrada in entradas:
                    entrada_hora_inicio = entrada.hora_inicio.hour
                    entrada_hora_finalizacion = entrada.hora_finalizacion.hour
                    for hora in range(entrada_hora_inicio,entrada_hora_finalizacion):
                        horas.append(datetime.time(hora,0))

                if hora_inicio in horas:
                    self.add_error('hora_inicio','Hay un registro en el intervalo de horas')

            else:
                self.add_error('actividades_entrada','Las actividades planeadas superan las horas disponibles')
                self.add_error('hora_inicio','Las actividades planeadas superan las horas disponibles')
        else:
            self.add_error('actividades_entrada','Debes seleccionar por lo menos una actividad')


    def __init__(self, *args, **kwargs):
        super(EntradaCronogramaform, self).__init__(*args, **kwargs)
        formador = Formador.objects.get(id=kwargs['initial']['formador'])

        semana = Semana.objects.get(id=kwargs['initial']['semana'])

        self.fields['formador'].initial = formador
        self.fields['semana'].initial = semana

        if 'data' in kwargs:
            if kwargs['data']['departamento'] != "":
                self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id = kwargs['data']['departamento']).values_list('id','nombre')
            if kwargs['data']['municipio'] != "":
                departamento_id = Municipio.objects.get(id=kwargs['data']['municipio']).departamento.id
                id_municipios = Municipio.objects.filter(departamento__id = departamento_id).values_list('id',flat=True)
                secretarias = Secretaria.objects.filter(municipio__id__in = id_municipios).values_list('id','nombre')
                self.fields['secretaria'].widget.choices = secretarias
            self.fields['fecha'].widget.attrs['initial'] = kwargs['data']['fecha']
        else:
            self.fields['municipio'].widget.choices = (('','---------'),)
            self.fields['secretaria'].widget.choices = (('','---------'),)

        departamentos = [('','----------')]

        for departamento in Departamento.objects.filter(id__in=formador.departamentos.values_list('id',flat=True)):
            departamentos.append((departamento.id,departamento.nombre))

        self.fields['departamento'].widget.choices = departamentos
        self.fields['departamento'].initial = ''


        grupos_choices = []
        for grupo in Grupos.objects.filter(formador=formador,oculto=False):
            grupos_choices.append((grupo.id,grupo.formador.codigo_ruta+'-'+grupo.nombre))
        self.fields['grupo'].widget.choices = grupos_choices

        tipo = 0
        if formador.cargo.nombre == "Formador Tipo 1":
            tipo = 1
        if formador.cargo.nombre == "Formador Tipo 2":
            tipo = 2
        if formador.cargo.nombre == "Formador Tipo 3":
            tipo = 3
        if formador.cargo.nombre == "Formador Tipo 4":
            tipo = 4

        self.fields['nivel'].widget.choices = Nivel.objects.filter(diplomado__numero = tipo).exclude(nombre="Nivel 0").values_list('id','nombre')

        actividades = []

        for actividad in Actividades.objects.filter(sesion__nivel__diplomado__numero = tipo).exclude(tipo = "Virtual"):
            actividades.append((actividad.id,actividad.sesion.nivel.nombre + " - " + actividad.sesion.nombre + " - " + "#" + str(actividad.numero) + " - Horas: " + str(actividad.horas) + " - " + actividad.nombre[:100]))

        self.fields['actividades_entrada'].widget.choices = actividades

        horas = []

        for hora in range(6,12):
            horas.append((str(hora)+":00",str(hora) + ':00 Am'))

        horas.append(('12:00','12:00 M'))

        for hora in range(13,23):
            horas.append((str(hora)+":00",str(hora-12) + ':00 Pm'))

        self.fields['hora_inicio'].widget.choices = horas


        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Registro cronograma',
                Div(
                    Div('semana',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('formador',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('departamento',css_class='col-sm-4'),
                    Div('municipio',css_class='col-sm-4'),
                    Div('secretaria',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('actividades_entrada',css_class='col-sm-3'),
                    Div('grupo',css_class='col-sm-3'),
                    Div('numero_sedes',css_class='col-sm-3'),
                    Div('beneficiados',css_class='col-sm-3'),
                    css_class = 'row'
                ),
                Div(
                    Div('nivel',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),

                Div(
                    Div('fecha',css_class='col-sm-3'),
                    Div('hora_inicio',css_class='col-sm-3'),
                    Div('institucion',css_class='col-sm-6'),

                    css_class = 'row'
                ),
                Div(
                    Div('direccion',css_class='col-sm-4'),
                    Div('telefono',css_class='col-sm-4'),
                    Div('ubicacion',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('hora_finalizacion',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
                Div(

                    css_class = 'row'
                ),
                Div(
                    Div('observaciones',css_class='col-sm-12'),
                    css_class = 'row'
                ),

            ),
        )

    class Meta:
        model = EntradaCronograma
        fields = '__all__'

        widgets = {
            'hora_inicio': forms.Select(),
            'ubicacion': forms.Select(choices=(('Urbana','Urbana'),('Rural','Rural'))),
            'fecha': forms.DateInput(attrs={'initial':''})
        }

class EntradaCronogramaUpdateform(forms.ModelForm):

    def clean(self):
        cleaned_data = super(EntradaCronogramaUpdateform, self).clean()
        actividades = cleaned_data.get('actividades_entrada')
        hora_inicio = cleaned_data.get('hora_inicio')
        formador = cleaned_data.get('formador')
        fecha = cleaned_data.get('fecha')

        id_actividades = []
        delta = 0
        if len(actividades) != 0:
            for actividad in actividades:
                id_actividades.append(actividad.id)

            tiempo = Actividades.objects.filter(id__in=id_actividades).values_list('horas',flat=True)
            delta = sum(tiempo)

            if hora_inicio.hour + delta <= 22:
                horas = []
                entradas = EntradaCronograma.objects.filter(formador=formador,fecha=fecha).exclude(id=self.instance.id)

                for entrada in entradas:
                    entrada_hora_inicio = entrada.hora_inicio.hour
                    entrada_hora_finalizacion = entrada.hora_finalizacion.hour
                    for hora in range(entrada_hora_inicio,entrada_hora_finalizacion):
                        horas.append(datetime.time(hora,0))

                if hora_inicio in horas:
                    self.add_error('hora_inicio','Hay un registro en el intervalo de horas')

            else:
                self.add_error('actividades_entrada','Las actividades planeadas superan las horas disponibles')
                self.add_error('hora_inicio','Las actividades planeadas superan las horas disponibles')
        else:
            self.add_error('actividades_entrada','Debes seleccionar por lo menos una actividad')


    def __init__(self, *args, **kwargs):
        super(EntradaCronogramaUpdateform, self).__init__(*args, **kwargs)

        formador = Formador.objects.get(id=kwargs['initial']['formador'])
        semana = Semana.objects.get(id=kwargs['initial']['semana'])

        self.fields['formador'].initial = formador
        self.fields['semana'].initial = semana
        self.fields['fecha'].widget.attrs['initial'] = kwargs['initial']['fecha'].strftime('%d/%m/%Y')

        if 'data' in kwargs:
            if kwargs['data']['departamento'] != "":
                self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id = kwargs['data']['departamento']).values_list('id','nombre')
            if kwargs['data']['municipio'] != "":
                departamento_id = Municipio.objects.get(id=kwargs['data']['municipio']).departamento.id
                id_municipios = Municipio.objects.filter(departamento__id = departamento_id).values_list('id',flat=True)
                secretarias = Secretaria.objects.filter(municipio__id__in = id_municipios).values_list('id','nombre')
                self.fields['secretaria'].widget.choices = secretarias
            self.fields['fecha'].widget.attrs['initial'] = kwargs['data']['fecha']
        else:
            self.fields['municipio'].widget.choices = Municipio.objects.filter(departamento__id = self.initial['departamento']).values_list('id','nombre')
            id_municipios = Municipio.objects.filter(departamento__id = self.initial['departamento']).values_list('id',flat=True)
            secretarias = Secretaria.objects.filter(municipio__id__in = id_municipios).values_list('id','nombre')
            self.fields['secretaria'].widget.choices = secretarias

        departamentos = []

        for departamento in Departamento.objects.filter(id__in=formador.departamentos.values_list('id',flat=True)):
            departamentos.append((departamento.id,departamento.nombre))

        self.fields['departamento'].widget.choices = departamentos
        self.fields['departamento'].initial = ''

        grupos_choices = []
        for grupo in Grupos.objects.filter(formador=formador,oculto=False):
            grupos_choices.append((grupo.id,grupo.formador.codigo_ruta+'-'+grupo.nombre))
        self.fields['grupo'].widget.choices = grupos_choices


        tipo = 0
        if formador.cargo.nombre == "Formador Tipo 1":
            tipo = 1
        if formador.cargo.nombre == "Formador Tipo 2":
            tipo = 2
        if formador.cargo.nombre == "Formador Tipo 3":
            tipo = 3
        if formador.cargo.nombre == "Formador Tipo 4":
            tipo = 4

        self.fields['nivel'].widget.choices = Nivel.objects.filter(diplomado__numero = tipo).exclude(nombre="Nivel 0").values_list('id','nombre')

        actividades = []

        for actividad in Actividades.objects.filter(sesion__nivel__diplomado__numero = tipo).exclude(tipo = "Virtual"):
            actividades.append((actividad.id,actividad.sesion.nivel.nombre + " - " + actividad.sesion.nombre + " - " + "#" + str(actividad.numero) + " - Horas: " + str(actividad.horas) + " - " + actividad.nombre[:100]))

        self.fields['actividades_entrada'].widget.choices = actividades

        horas = []

        for hora in range(6,12):
            horas.append((str(hora)+":00",str(hora) + ':00 Am'))

        horas.append(('12:00','12:00 M'))

        for hora in range(13,23):
            horas.append((str(hora)+":00",str(hora-12) + ':00 Pm'))

        self.fields['hora_inicio'].widget.choices = horas
        x = EntradaCronograma.objects.get(id = kwargs['initial']['id']).hora_inicio.hour
        self.initial['hora_inicio'] = str(x) + ":00"
        self.fields['hora_inicio'].initial = str(x) + ":00"



        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Registro cronograma',
                Div(
                    Div('semana',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('formador',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
                Div(
                    Div('departamento',css_class='col-sm-4'),
                    Div('municipio',css_class='col-sm-4'),
                    Div('secretaria',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('actividades_entrada',css_class='col-sm-3'),
                    Div('grupo',css_class='col-sm-3'),
                    Div('numero_sedes',css_class='col-sm-3'),
                    Div('beneficiados',css_class='col-sm-3'),
                    css_class = 'row'
                ),
                Div(
                    Div('nivel',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),

                Div(
                    Div('fecha',css_class='col-sm-3'),
                    Div('hora_inicio',css_class='col-sm-3'),
                    Div('institucion',css_class='col-sm-6'),

                    css_class = 'row'
                ),
                Div(
                    Div('direccion',css_class='col-sm-4'),
                    Div('telefono',css_class='col-sm-4'),
                    Div('ubicacion',css_class='col-sm-4'),
                    css_class = 'row'
                ),
                Div(
                    Div('hora_finalizacion',css_class='col-sm-12'),
                    css_class = 'hidden'
                ),
                Div(

                    css_class = 'row'
                ),
                Div(
                    Div('observaciones',css_class='col-sm-12'),
                    css_class = 'row'
                ),

            ),
        )

    class Meta:
        model = EntradaCronograma
        fields = '__all__'

        widgets = {
            'hora_inicio': forms.Select(),
            'ubicacion': forms.Select(choices=(('Urbana','Urbana'),('Rural','Rural'))),
            'fecha': forms.DateInput(attrs={'initial':''})
        }