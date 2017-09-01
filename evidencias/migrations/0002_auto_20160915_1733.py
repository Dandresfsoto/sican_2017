# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-15 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0004_actividades'),
        ('matrices', '0001_initial'),
        ('evidencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigoevidencia',
            name='beneficiarios',
            field=models.ManyToManyField(to='matrices.Beneficiario'),
        ),
        migrations.AddField(
            model_name='codigoevidencia',
            name='entregable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entregable_diplomado', to='productos.Entregable'),
        ),
        migrations.AddField(
            model_name='codigoevidencia',
            name='red',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='red_evidencia', to='evidencias.Red'),
        ),
    ]
