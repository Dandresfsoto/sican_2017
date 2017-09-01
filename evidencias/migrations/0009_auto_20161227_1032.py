# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-27 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evidencias', '0008_subsanacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subsanacion',
            name='evidencia',
        ),
        migrations.AddField(
            model_name='evidencia',
            name='cantidad_cargados',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evidencia',
            name='subsanacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subsanacion',
            name='evidencia_origen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='evidencia_origen', to='evidencias.Evidencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subsanacion',
            name='evidencia_subsanada',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='evidencia_subsanada', to='evidencias.Evidencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subsanacion',
            name='red',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='evidencias.Red'),
            preserve_default=False,
        ),
    ]
