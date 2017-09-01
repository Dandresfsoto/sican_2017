# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-26 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0004_actividades'),
        ('formadores', '0005_auto_20160826_0829'),
        ('municipios', '0001_initial'),
        ('formacion', '0001_initial'),
        ('secretarias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradacronograma',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formadores.Grupos'),
        ),
        migrations.AddField(
            model_name='entradacronograma',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipios.Municipio'),
        ),
        migrations.AddField(
            model_name='entradacronograma',
            name='nivel',
            field=models.ManyToManyField(blank=True, to='productos.Nivel'),
        ),
        migrations.AddField(
            model_name='entradacronograma',
            name='secretaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secretarias.Secretaria'),
        ),
        migrations.AddField(
            model_name='entradacronograma',
            name='semana',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semana_cronograma', to='formacion.Semana'),
        ),
    ]
