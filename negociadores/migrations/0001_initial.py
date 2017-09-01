# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-20 20:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('region', '0002_auto_20160728_1439'),
        ('bancos', '0002_auto_20160714_1358'),
        ('rh', '0003_auto_20160728_1439'),
        ('cargos', '0004_auto_20160728_1439'),
        ('departamentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Negociador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_ruta', models.CharField(blank=True, max_length=100, null=True)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('cedula', models.BigIntegerField(unique=True)),
                ('correo_personal', models.EmailField(blank=True, max_length=100)),
                ('celular_personal', models.CharField(blank=True, max_length=100)),
                ('profesion', models.CharField(blank=True, max_length=100)),
                ('fecha_contratacion', models.DateField(blank=True, null=True)),
                ('fecha_terminacion', models.DateField(blank=True, null=True)),
                ('tipo_cuenta', models.CharField(blank=True, max_length=100)),
                ('numero_cuenta', models.CharField(blank=True, max_length=100)),
                ('eps', models.CharField(blank=True, max_length=100)),
                ('pension', models.CharField(blank=True, max_length=100)),
                ('arl', models.CharField(blank=True, max_length=100)),
                ('oculto', models.BooleanField(default=False)),
                ('banco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bancos.Banco')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargos.Cargo')),
                ('departamentos', models.ManyToManyField(blank=True, related_name='departamento_negociador', to='departamentos.Departamento')),
                ('lider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.Region')),
            ],
            options={
                'ordering': ['nombres'],
            },
        ),
        migrations.CreateModel(
            name='Soporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creacion', models.DateField(auto_now=True)),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField(blank=True, max_length=1000)),
                ('oculto', models.BooleanField(default=False)),
                ('archivo', models.FileField(blank=True, upload_to='Negociadores/Soportes/')),
                ('negociador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='negociadores.Negociador')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soporte_negociador', to='rh.TipoSoporte')),
            ],
            options={
                'ordering': ['negociador'],
            },
        ),
    ]
