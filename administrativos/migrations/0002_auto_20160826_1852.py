# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-26 23:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rh', '0003_auto_20160728_1439'),
        ('administrativos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Soporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creacion', models.DateField(auto_now=True)),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField(blank=True, max_length=1000)),
                ('oculto', models.BooleanField(default=False)),
                ('archivo', models.FileField(blank=True, upload_to='Administratios/Soportes/')),
            ],
            options={
                'ordering': ['administrativo'],
            },
        ),
        migrations.AlterModelOptions(
            name='administrativo',
            options={'ordering': ['nombres']},
        ),
        migrations.AlterField(
            model_name='administrativo',
            name='banco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bancos.Banco'),
        ),
        migrations.AddField(
            model_name='soporte',
            name='administrativo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativos.Administrativo'),
        ),
        migrations.AddField(
            model_name='soporte',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rh.TipoSoporte'),
        ),
    ]
