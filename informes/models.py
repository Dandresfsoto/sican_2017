from __future__ import unicode_literals

from django.db import models
from usuarios.models import User
import os

# Create your models here.
class InformesExcel(models.Model):
    usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length=100)
    progreso = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='Informes/',blank=True,null=True)
    creacion = models.DateTimeField(auto_now=True)
    id_task = models.CharField(max_length=100,blank=True)

    class Meta:
        ordering = ['creacion']

    def __unicode__(self):
        return self.usuario.email

    def get_archivo_url(self):
        try:
            url = self.archivo.url
        except:
            url = ""
        return url


    def archivo_filename(self):
        return os.path.basename(self.archivo.name)