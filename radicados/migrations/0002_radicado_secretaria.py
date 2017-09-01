# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-28 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('radicados', '0001_initial'),
        ('secretarias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='radicado',
            name='secretaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secretarias.Secretaria'),
        ),
    ]
