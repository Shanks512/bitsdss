# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-18 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_code',
            field=models.CharField(default='CS101', max_length=10),
        ),
    ]
