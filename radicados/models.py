from __future__ import unicode_literals

from django.db import models
from municipios.models import Municipio
from secretarias.models import Secretaria
# Create your models here.
class Radicado(models.Model):
    numero = models.BigIntegerField(unique=True)
    secretaria = models.ForeignKey(Secretaria)
    municipio = models.ForeignKey(Municipio)

    dane_sede = models.BigIntegerField(blank=True,null=True)
    sede_id = models.BigIntegerField(blank=True,null=True)
    nombre_sede = models.CharField(max_length=200,blank=True,null=True)

    dane_ie = models.BigIntegerField(blank=True,null=True)
    ie_id = models.BigIntegerField(blank=True,null=True)
    nombre_ie = models.CharField(max_length=200,blank=True,null=True)

    zona = models.CharField(max_length=200,blank=True,null=True)
    matricula = models.BigIntegerField(blank=True,null=True)
    direccion = models.CharField(max_length=200,blank=True,null=True)

    tipo = models.IntegerField(blank=True,null=True)
    ubicacion = models.IntegerField(blank=True,null=True)
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre_sede']

    def __unicode__(self):
        return unicode(self.numero) + ' - ' + self.nombre_sede

class RadicadoRetoma(models.Model):
    numero = models.BigIntegerField()
    municipio = models.ForeignKey(Municipio)
    ubicacion = models.CharField(max_length=300)
    institucion = models.CharField(max_length=300)
    sede = models.CharField(max_length=300)
    nombre_completo = models.CharField(max_length=300)
    dane = models.BigIntegerField()

    class Meta:
        ordering = ['numero']

    def __unicode__(self):
        return str(self.numero)