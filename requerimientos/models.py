from __future__ import unicode_literals

from django.db import models
from region.models import Region
from usuarios.models import User
from datetime import datetime

# Create your models here.

class Requerimiento(models.Model):
    creacion = models.DateTimeField(auto_now_add = True)

    recepcion_solicitud = models.DateField()
    region = models.ManyToManyField(Region,related_name='region_requerimiento')
    entidad_remitente = models.CharField(max_length=100)
    funcionario_remitente = models.CharField(max_length=100,blank=True,null=True)
    nombre = models.CharField(max_length=100)
    archivo_solicitud = models.FileField(upload_to='Requerimientos/Interventoria',blank=True,null=True)
    descripcion = models.TextField(max_length=5000,blank=True,null=True)

    tiempo_respuesta = models.IntegerField()
    encargados = models.ManyToManyField(User,related_name='encargados_requerimiento')
    medio_entrega = models.CharField(max_length=100)

    estado = models.CharField(max_length=100,blank=True,null=True,default='Abierto')
    fecha_respuesta = models.DateField(blank=True,null=True)
    observaciones = models.TextField(max_length=1000,blank=True,null=True)
    archivo_respuesta = models.FileField(upload_to='Requerimientos/Interventoria',blank=True,null=True)

    def __unicode__(self):
        return self.nombre

    def get_archivo_solicitud_url(self):
        try:
            url = self.archivo_solicitud.url
        except:
            url = ""
        return url

    def get_archivo_respuesta_url(self):
        try:
            url = self.archivo_respuesta.url
        except:
            url = ""
        return url

    def get_region_string(self):
        value = ''
        for region in self.region.values_list('numero',flat=True):
            value = value + unicode(region) + ', '
        return value[:-2]

    def get_encargados_string(self):
        value = ''
        for encargado in self.encargados.values_list('first_name',flat=True):
            value = value + unicode(encargado) + ', '
        return value[:-2]

    def get_dias_mora(self):
        mora = datetime.now().date() - self.recepcion_solicitud
        return mora.days - self.tiempo_respuesta