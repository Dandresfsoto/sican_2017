# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-29 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import vigencia2017.models


class Migration(migrations.Migration):

    dependencies = [
        ('vigencia2017', '0008_auto_20170827_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='CargaMasiva2017',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='Evidencias/Vigencia 2017/Carga Masiva')),
            ],
        ),
        migrations.AlterField(
            model_name='evidencia',
            name='archivo',
            field=models.FileField(upload_to=vigencia2017.models.evidencia_directory),
        ),
    ]
