from __future__ import unicode_literals

from django.db import models
from municipios.models import Municipio

# Create your models here.
class Secretaria(models.Model):
    municipio = models.ForeignKey(Municipio)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    web = models.URLField(max_length=200)
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre