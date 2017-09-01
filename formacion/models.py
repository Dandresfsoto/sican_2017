from __future__ import unicode_literals

from django.db import models
from formadores.models import Formador, Grupos
from departamentos.models import Departamento
from municipios.models import Municipio
from secretarias.models import Secretaria
from productos.models import Nivel, Actividades
import datetime
from isoweek import Week
from evidencias.models import Red
from matrices.models import Beneficiario

# Create your models here.

class Semana(models.Model):
    creacion = models.DateTimeField(auto_now=True)
    numero = models.IntegerField()

    def __unicode__(self):
        return unicode(self.numero)

    def get_rango_semana(self):
        inicio = Week(self.creacion.year,self.numero).monday()
        fin = Week(self.creacion.year,self.numero).sunday()
        return


class EntradaCronograma(models.Model):
    semana = models.ForeignKey(Semana,related_name='semana_cronograma')
    formador = models.ForeignKey(Formador)
    departamento = models.ForeignKey(Departamento)
    municipio = models.ForeignKey(Municipio)
    secretaria = models.ForeignKey(Secretaria)
    grupo = models.ForeignKey(Grupos)
    numero_sedes = models.IntegerField()
    nivel = models.ManyToManyField(Nivel,blank=True)
    actividades_entrada = models.ManyToManyField(Actividades,related_name='actividades_cronograma',blank=True)
    beneficiados = models.IntegerField()
    fecha = models.DateField()
    institucion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=100,blank=True)
    hora_inicio = models.TimeField()
    hora_finalizacion = models.TimeField(blank=True,null=True)
    ubicacion = models.CharField(max_length=100)
    observaciones = models.TextField(max_length=1000,blank=True)


