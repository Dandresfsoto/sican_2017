# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-22 02:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('negociadores', '0002_auto_20170214_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='soporte',
            name='contrato',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='negociadores.Contrato'),
        ),
    ]
