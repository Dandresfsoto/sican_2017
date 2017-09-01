#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from usuarios.extra import ContentTypeRestrictedFileField
import os
from sican.settings.base import STATIC_URL
from cargos.models import Cargo
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from departamentos.models import Departamento
from municipios.models import Municipio
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        try:
            user = self.get(email=email)
        except:
            user = self.create(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    objects = UserManager()
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    cargo = models.ForeignKey(Cargo,default=1)
    telefono_corporativo = models.CharField(max_length=10,blank=True)
    telefono_personal = models.CharField(max_length=10,blank=True)
    correo_personal = models.EmailField(max_length=100,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    recovery = models.CharField(max_length=20,null=True,blank=True,default="")
    new_password = models.CharField(max_length=100,null=True,blank=True,default="")
    photo = ContentTypeRestrictedFileField(upload_to='Usuarios/Foto',blank=True,null=True,content_types=['image/jpg', 'image/jpeg', 'image/png'],max_upload_size=10485760)

    numero_contrato = models.CharField(max_length=100,blank=True,null=True)
    fecha_inicio = models.DateField(blank=True,null=True)
    fecha_terminacion = models.DateField(blank=True,null=True)
    fecha_nacimiento = models.DateField(blank=True,null=True)
    departamento_natal = models.ForeignKey(Departamento,blank=True,null=True)
    municipio_natal = models.ForeignKey(Municipio,blank=True,null=True)
    genero = models.CharField(max_length=100,blank=True,null=True)
    tipo_sangre = models.CharField(max_length=100,blank=True,null=True)
    cedula = models.BigIntegerField(blank=True,null=True)

    skype = models.CharField(max_length=100,blank=True,null=True)
    facebook = models.CharField(max_length=100,blank=True,null=True)
    twitter = models.CharField(max_length=100,blank=True,null=True)
    whatsapp = models.CharField(max_length=100,blank=True,null=True)
    email_corporativo = models.EmailField(max_length=100,blank=True)

    departamento_residencia = models.ForeignKey(Departamento,blank=True,null=True,related_name='departamento_residencia')
    municipio_residencia = models.ForeignKey(Municipio,blank=True,null=True,related_name='municipio_residencia')
    direccion_residencia = models.CharField(max_length=100,blank=True,null=True)
    barrio_residencia = models.CharField(max_length=100,blank=True,null=True)
    telefono_residencia = models.CharField(max_length=100,blank=True,null=True)
    celular_residencia = models.CharField(max_length=100,blank=True,null=True)
    nombre_contacto_residencia = models.CharField(max_length=100,blank=True,null=True)
    telefono_contacto_residencia = models.CharField(max_length=100,blank=True,null=True)
    celular_contacto_residencia = models.CharField(max_length=100,blank=True,null=True)

    departamento_residencia_temporal = models.ForeignKey(Departamento,blank=True,null=True,related_name='departamento_residencia_temporal')
    municipio_residencia_temporal = models.ForeignKey(Municipio,blank=True,null=True,related_name='municipio_residencia_temporal')
    direccion_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)
    barrio_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)
    telefono_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)
    celular_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)
    nombre_contacto_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)
    telefono_contacto_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)
    celular_contacto_residencia_temporal = models.CharField(max_length=100,blank=True,null=True)

    empresa_transporte = models.CharField(max_length=100,blank=True,null=True)
    horarios_transporte = models.TextField(max_length=5000,blank=True,null=True)
    tiempo_transporte = models.CharField(max_length=100,blank=True,null=True)
    valor_transporte = models.CharField(max_length=100,blank=True,null=True)

    informacion_adicional = models.TextField(max_length=5000,blank=True,null=True)


    class Meta:
        ordering = ['first_name']

    def get_full_name(self):
        return self.email

    def get_full_name_string(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.email

    def photo_filename(self):
        return os.path.basename(self.photo.name)

    def get_photo(self):
        photo = self.photo
        if photo.name == '':
            avatar = STATIC_URL+"img/andes_user.jpg"
        else:
            avatar = photo.url
        return avatar

    def get_url_photo(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url

    def photo_filename(self):
        return os.path.basename(self.photo.name)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
            Token.objects.create(user=instance)