# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20160220_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timewindow',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timewindow',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
