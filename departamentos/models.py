from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Departamento(models.Model):
    codigo_auditoria = models.IntegerField()
    codigo_pais = models.IntegerField()
    codigo_departamento = models.IntegerField()
    nombre = models.CharField(max_length=100)
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre