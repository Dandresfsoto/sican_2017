from __future__ import unicode_literals

from django.db import models
from preinscripcion.models import DocentesPreinscritos

# Create your models here.
class PercepcionInicial(models.Model):
    docente_preinscrito = models.ForeignKey(DocentesPreinscritos)
    area = models.CharField(max_length=1000,blank=True)
    area_1 = models.CharField(max_length=1000,blank=True)
    antiguedad = models.CharField(max_length=1000,blank=True)
    pregunta_1 = models.CharField(max_length=1000,blank=True)
    pregunta_1_1 = models.CharField(max_length=1000,blank=True)
    pregunta_2 = models.CharField(max_length=1000,blank=True)
    pregunta_3 = models.CharField(max_length=1000,blank=True)
    pregunta_4 = models.CharField(max_length=1000,blank=True)
    pregunta_5 = models.CharField(max_length=1000,blank=True)
    pregunta_6 = models.CharField(max_length=1000,blank=True)
    pregunta_6_1 = models.CharField(max_length=1000,blank=True)
    pregunta_7 = models.CharField(max_length=1000,blank=True)
    pregunta_8 = models.CharField(max_length=1000,blank=True)
    pregunta_9 = models.CharField(max_length=1000,blank=True)
    pregunta_10 = models.CharField(max_length=1000,blank=True)
    pregunta_11 = models.CharField(max_length=1000,blank=True)
    pregunta_12 = models.CharField(max_length=1000,blank=True)
    pregunta_12_1 = models.CharField(max_length=1000,blank=True)
    pregunta_13 = models.CharField(max_length=1000,blank=True)

    def __unicode__(self):
        return unicode(self.docente_preinscrito.cedula)

    class Meta:
        ordering = ['docente_preinscrito__primer_nombre']


class PercepcionFinal(models.Model):
    docente_preinscrito = models.ForeignKey(DocentesPreinscritos)
    area = models.CharField(max_length=1000,blank=True)
    tiempo_formacion = models.CharField(max_length=1000,blank=True)
    pregunta_1 = models.CharField(max_length=1000,blank=True)
    pregunta_2 = models.CharField(max_length=1000,blank=True)
    pregunta_3 = models.CharField(max_length=1000,blank=True)
    pregunta_4 = models.CharField(max_length=1000,blank=True)
    pregunta_5 = models.CharField(max_length=1000,blank=True)
    pregunta_6 = models.CharField(max_length=1000,blank=True)
    pregunta_7 = models.CharField(max_length=1000,blank=True)
    pregunta_8 = models.CharField(max_length=1000,blank=True)
    pregunta_9 = models.CharField(max_length=1000,blank=True)
    pregunta_10 = models.CharField(max_length=1000,blank=True)
    pregunta_11 = models.CharField(max_length=1000,blank=True)
    pregunta_12 = models.CharField(max_length=1000,blank=True)

    def __unicode__(self):
        return unicode(self.docente_preinscrito.cedula)

    class Meta:
        ordering = ['docente_preinscrito__primer_nombre']