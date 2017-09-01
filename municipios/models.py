from __future__ import unicode_literals

from django.db import models
from departamentos.models import Departamento

# Create your models here.
class Municipio(models.Model):
    departamento = models.ForeignKey(Departamento)
    codigo_auditoria = models.IntegerField()
    codigo_municipio = models.BigIntegerField()
    nombre = models.CharField(max_length=100)
    oculto = models.BooleanField()

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre + ', ' + self.departamento.nombre