from __future__ import unicode_literals

from django.db import models
from usuarios.models import User

# Create your models here.

class Mensaje(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    de = models.ForeignKey(User,related_name="mensaje_de")
    para = models.ForeignKey(User,related_name="mensaje_para")
    texto = models.TextField(max_length=1000)