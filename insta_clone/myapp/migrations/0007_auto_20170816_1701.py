# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 00:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20170816_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='caption',
            field=models.CharField(max_length=240),
        ),
    ]
