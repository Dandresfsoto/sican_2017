from __future__ import unicode_literals

from django.db import models
from usuarios.models import User
from formadores.models import Formador
from evidencias.models import Diplomado
from region.models import Region
from radicados.models import Radicado
from formadores.models import Contrato

# Create your models here.

class GruposBeneficiarios(models.Model):
    usuario = models.ForeignKey(User)
    diplomado_grupo = models.ForeignKey(Diplomado)
    contrato = models.ForeignKey(Contrato,null=True)
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=500,blank=True,null=True)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre



class BeneficiarioVigencia(models.Model):
    grupo = models.ForeignKey(GruposBeneficiarios, related_name='grupo_beneficiario')

    cedula = models.BigIntegerField(unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=100, blank=True, null=True)
    telefono_celular = models.CharField(max_length=100, blank=True, null=True)

    radicado = models.ForeignKey(Radicado,blank=True,null=True)



    area = models.CharField(max_length=100,blank=True,null=True)
    grado = models.CharField(max_length=100,blank=True,null=True)
    genero = models.CharField(max_length=100,blank=True,null=True)
    estado = models.CharField(max_length=100,blank=True,null=True)


    def __unicode__(self):
        return str(self.cedula) + ' - ' + self.nombres + ' ' + self.apellidos

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos

    def get_grupo(self):
        return self.ruta + '-' + self.grupo.nombre

    def get_diploma_url(self):
        try:
            url = self.diploma.url
        except:
            url = ""
        return url

    def get_diploma_url_rest(self):
        try:
            url = self.diploma.url
        except:
            url = None
        return url

    def diplomado_name(self):
        return self.diplomado.nombre