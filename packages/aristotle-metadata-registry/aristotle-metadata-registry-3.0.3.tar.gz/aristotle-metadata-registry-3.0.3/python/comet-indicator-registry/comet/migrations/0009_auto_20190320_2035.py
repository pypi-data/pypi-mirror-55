# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-20 09:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comet', '0008_auto_20190218_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qualitystatement',
            name='implementationEndDate',
        ),
        migrations.RemoveField(
            model_name='qualitystatement',
            name='implementationStartDate',
        ),
    ]
