from __future__ import unicode_literals
from radicados.models import RadicadoRetoma
from django.db import models
from usuarios.models import User

# Create your models here.

class Retoma(models.Model):
    radicado = models.ForeignKey(RadicadoRetoma)
    lider = models.ForeignKey(User)
    formato_solicitud = models.FileField(upload_to='Acceso/Retoma/Seleccion',blank=True,null=True)
    cantidad_equipos = models.IntegerField(blank=True)
    estado_seleccion = models.CharField(max_length=100,default='Revision')

    def __unicode__(self):
        return self.radicado.numero