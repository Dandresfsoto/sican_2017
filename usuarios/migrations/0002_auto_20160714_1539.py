# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-14 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cargo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cargos.Cargo'),
        ),
    ]
