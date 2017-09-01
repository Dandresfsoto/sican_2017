from __future__ import unicode_literals

from django.db import models
import os

# Create your models here.
class Cargo(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=1000,blank=True)
    manual = models.FileField(upload_to="Manual Funciones",blank=True)
    oculto = models.BooleanField(default=False)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    def get_url_manual(self):
        try:
            url = self.manual.url
        except:
            url = ''
        return url

    def manual_filename(self):
        return os.path.basename(self.manual.name)