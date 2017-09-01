from __future__ import unicode_literals

from django.db import models
from departamentos.models import Departamento
from municipios.models import Municipio
from radicados.models import Radicado

# Create your models here.
class DocentesMinEducacion(models.Model):
    cedula = models.BigIntegerField(unique=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100,blank=True)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100,blank=True)
    cargo = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100,blank=True,null=True)
    telefono_fijo = models.BigIntegerField(blank=True,null=True)
    telefono_celular = models.BigIntegerField(blank=True,null=True)
    departamento = models.ForeignKey(Departamento,blank=True,null=True)
    municipio = models.ForeignKey(Municipio,blank=True,null=True)
    radicado = models.ForeignKey(Radicado,blank=True,null=True)

    class Meta:
        ordering = ['primer_apellido']

    def __unicode__(self):
        return ("%s %s %s %s") % (self.primer_nombre,self.segundo_nombre,self.primer_apellido, self.segundo_apellido)

class DocentesDocentic(models.Model):
    cedula = models.BigIntegerField(unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    formador = models.CharField(max_length=100)
    cedula_formador = models.BigIntegerField()
    directivo = models.BooleanField(default=False)
    informatica = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombres']

    def __unicode__(self):
        return str(self.cedula)