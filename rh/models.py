from __future__ import unicode_literals

from django.db import models
from usuarios.models import User
from municipios.models import Municipio
from departamentos.models import Departamento
import os

# Create your models here.
class TipoSoporte(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500,blank=True)
    categoria = models.CharField(max_length=100,blank=True,null=True)
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre


class RequerimientoPersonal(models.Model):
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    solicitante = models.ForeignKey(User)

    departamento = models.ForeignKey(Departamento)
    municipios = models.ManyToManyField(Municipio)
    codigo_ruta = models.CharField(max_length=100)
    encargado = models.ForeignKey(User,related_name='encargado_requerimiento')
    observacion_solicitante = models.TextField(max_length=500,blank=True,null=True)

    fecha_respuesta = models.DateTimeField(blank=True,null=True)
    nombre = models.CharField(max_length=100,blank=True,null=True)
    cedula = models.BigIntegerField(blank=True,null=True)
    celular = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    hv = models.FileField(upload_to="Cantidatos/Hv",blank=True,null=True)
    observacion_respuesta = models.TextField(max_length=500,blank=True,null=True)

    fecha_solicitud_contratacion = models.DateTimeField(blank=True,null=True)
    observacion_final = models.TextField(max_length=500,blank=True,null=True)

    remitido_respuesta = models.BooleanField(default=False)
    remitido_contratacion = models.BooleanField(default=False)
    contratar = models.BooleanField(default=False)
    desierto = models.BooleanField(default=False)
    contrato_enviado = models.BooleanField(default=False)
    contratado = models.BooleanField(default=False)


    def get_municipios_string(self):
        municipios = ''
        for municipio in self.municipios.all():
            municipios += municipio.nombre + ', '
        return municipios[:-2]


    def get_archivo_url(self):
        try:
            url = self.hv.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.hv.name)