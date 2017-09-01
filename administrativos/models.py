from __future__ import unicode_literals

from django.db import models
from region.models import Region
from cargos.models import Cargo
from bancos.models import Banco
from rh.models import TipoSoporte
import os
from usuarios.models import User

# Create your models here.

class Administrativo(models.Model):

    usuario = models.ForeignKey(User,blank=True,null=True,related_name='usuario_sistema_administrativo')

    #---------- REGION----------------------
    region = models.ManyToManyField(Region)

    #---------- DATOS PERSONALES----------------------
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.BigIntegerField()
    correo_personal = models.EmailField(max_length=100,blank=True)
    celular_personal = models.CharField(max_length=100,blank=True)

    #---------- INFORMACION PROFESIONAL ----------------------
    cargo = models.ForeignKey(Cargo)
    profesion = models.CharField(max_length=100,blank=True)
    correo_corporativo = models.EmailField(max_length=100,blank=True)
    celular_corporativo = models.CharField(max_length=100,blank=True)
    fecha_contratacion = models.DateField(null=True,blank=True)
    fecha_terminacion = models.DateField(null=True,blank=True)

    #---------- INFORMACION BANCARIA Y SEGURIDAD SOCIAL ----------------------
    banco = models.ForeignKey(Banco,blank=True,null=True)
    tipo_cuenta = models.CharField(max_length=100,blank=True)
    numero_cuenta = models.CharField(max_length=100,blank=True)

    eps = models.CharField(max_length=100,blank=True)
    pension = models.CharField(max_length=100,blank=True)
    arl = models.CharField(max_length=100,blank=True)

    usuario_colombia_aprende = models.CharField(max_length=100,blank=True)

    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombres']

    def __unicode__(self):
        return self.nombres

    def get_region_string(self):
        value = ''
        for region in self.region.values_list('nombre',flat=True):
            value = value + unicode(region) + ', '
        return value[:-2]

    def get_full_name(self):
        return self.nombres + " " + self.apellidos

class Soporte(models.Model):
    administrativo = models.ForeignKey(Administrativo)
    creacion = models.DateField(auto_now=True)
    fecha = models.DateField()
    tipo = models.ForeignKey(TipoSoporte)
    descripcion = models.TextField(max_length=1000,blank=True)
    oculto = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='Administratios/Soportes/',blank=True)

    class Meta:
        ordering = ['administrativo']

    def __unicode__(self):
        return self.administrativo.get_full_name()

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)

class SolicitudSoportes(models.Model):
    nombre = models.CharField(max_length=200)
    soportes_requeridos = models.ManyToManyField(TipoSoporte,related_name='soportes_requeridos_contratos_administrativos')

    def __unicode__(self):
        return self.nombre

class Contrato(models.Model):
    nombre = models.CharField(max_length=200)
    administrativo = models.ForeignKey(Administrativo)
    soportes_requeridos = models.ForeignKey(SolicitudSoportes)
    fecha = models.DateTimeField(auto_now_add = True)
    fecha_inicio = models.DateField(blank=True,null=True)
    fecha_fin = models.DateField(blank=True,null=True)
    renuncia = models.BooleanField(default=False)
    soporte_renuncia = models.FileField(upload_to='Contratos/Administrativos/Soporte Renuncia/',blank=True,null=True)
    liquidado = models.BooleanField(default=False)
    soporte_liquidacion = models.FileField(upload_to='Contratos/Administrativos/Soporte Liquidacion/',blank=True,null=True)