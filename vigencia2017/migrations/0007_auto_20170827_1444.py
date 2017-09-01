# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-27 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_entregable_escencial'),
        ('vigencia2017', '0006_auto_20170825_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evidencia',
            name='corte_id',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='evidencia',
        ),
        migrations.AddField(
            model_name='pago',
            name='corte_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pago',
            name='entregable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='productos.Entregable'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago',
            name='evidencia_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
