# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-06 22:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aristotle_mdr', '0051_auto_20190216_0455'),
    ]

    operations = [
        migrations.CreateModel(
            name='RAValidationRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rules', models.TextField(default='')),
                ('registration_authority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aristotle_mdr.RegistrationAuthority', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistryValidationRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rules', models.TextField(default='')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
