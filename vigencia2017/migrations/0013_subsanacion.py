# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-10-18 20:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vigencia2017', '0012_evidencia_completa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subsanacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('observacion', models.TextField(blank=True, max_length=1000)),
                ('evidencia_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencia_origen_2017', to='vigencia2017.Evidencia')),
                ('evidencia_subsanada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencia_subsanada_2017', to='vigencia2017.Evidencia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_2017', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
