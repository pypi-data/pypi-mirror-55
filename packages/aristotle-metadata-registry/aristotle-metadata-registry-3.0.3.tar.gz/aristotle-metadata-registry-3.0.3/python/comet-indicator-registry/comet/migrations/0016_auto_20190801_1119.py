# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-01 01:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comet', '0014_auto_20190716_0859'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicatordenominatordefinition',
            options={'verbose_name': 'Denominator'},
        ),
        migrations.AlterModelOptions(
            name='indicatordisaggregationdefinition',
            options={'verbose_name': 'Disaggregator'},
        ),
        migrations.AlterModelOptions(
            name='indicatornumeratordefinition',
            options={'verbose_name': 'Numerator'},
        ),
    ]
