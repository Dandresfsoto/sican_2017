# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-21 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formadores', '0015_auto_20161018_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='formador',
            name='expedicion',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
