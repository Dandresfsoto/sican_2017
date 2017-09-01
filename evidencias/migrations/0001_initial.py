# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-15 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0004_actividades'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoEvidencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='Evidencias/Soportes')),
            ],
        ),
        migrations.CreateModel(
            name='Red',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('descripcion', models.TextField(blank=True, max_length=1000)),
                ('diplomado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.Diplomado')),
            ],
        ),
    ]
