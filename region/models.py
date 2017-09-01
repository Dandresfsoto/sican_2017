from __future__ import unicode_literals

from django.db import models
from departamentos.models import Departamento

# Create your models here.
class Region(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    departamentos = models.ManyToManyField(Departamento)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre