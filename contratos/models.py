from __future__ import unicode_literals

from django.db import models
from productos.models import Entregable

# Create your models here.
class Contratos(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre


class EntregagleContrato(models.Model):
    contrato = models.ForeignKey(Contratos)
    entregable_contrato = models.ForeignKey(Entregable)
    valor = models.BigIntegerField()

    def __unicode__(self):
        return self.contrato