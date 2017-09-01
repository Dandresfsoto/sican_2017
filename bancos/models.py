from __future__ import unicode_literals

from django.db import models

class Banco(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre