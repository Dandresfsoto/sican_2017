# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rh', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiposoporte',
            name='oculto',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tiposoporte',
            name='descripcion',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
