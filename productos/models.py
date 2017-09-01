from __future__ import unicode_literals

from django.db import models
import os
from cargos.models import Cargo


# Create your models here.
class Diplomado(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return self.nombre

class Nivel(models.Model):
    diplomado = models.ForeignKey(Diplomado,related_name="nivel_diplomado")
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return ("%s - %s") % (self.diplomado.nombre,self.nombre)

class Sesion(models.Model):
    nivel = models.ForeignKey(Nivel,related_name="sesion_nivel")
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()

    def __unicode__(self):
        return ("%s - %s - %s") % (self.nivel.diplomado.nombre,self.nivel.nombre,self.nombre)

class Entregable(models.Model):
    sesion = models.ForeignKey(Sesion,related_name="entregable_sesion")
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=100)
    escencial = models.CharField(max_length=20,default='No')
    formato = models.FileField(upload_to="Entregables/Formatos",blank=True,null=True)

    def get_archivo_url(self):
        try:
            url = self.formato.url
        except:
            url = ""
        return url



    def archivo_filename(self):
        if self.formato != None:
            name = self.formato.name
        else:
            name = ""
        return os.path.basename(name)

class Actividades(models.Model):
    sesion = models.ForeignKey(Sesion,related_name="actividad_sesion")
    nombre = models.CharField(max_length=300)
    numero = models.IntegerField()
    tipo = models.CharField(max_length=100)
    horas = models.IntegerField()

    def __unicode__(self):
        return unicode(self.sesion.nombre + " - " + self.nombre)

class Contratos(models.Model):
    cargo = models.ForeignKey(Cargo)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)


    def __unicode__(self):
        return self.nombre + ' - ' + self.cargo.nombre

class ValorEntregable(models.Model):
    contrato = models.ForeignKey(Contratos,related_name='contrato_valor')
    entregable = models.ForeignKey(Entregable,related_name='entregable_valor')
    valor = models.FloatField()

    def __unicode__(self):
        return self.entregable.nombre