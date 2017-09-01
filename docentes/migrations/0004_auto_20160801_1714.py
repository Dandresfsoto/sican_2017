# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-01 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docentes', '0003_docentesdocentic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docentesmineducacion',
            name='correo',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='docentesmineducacion',
            name='telefono_celular',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='docentesmineducacion',
            name='telefono_fijo',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
