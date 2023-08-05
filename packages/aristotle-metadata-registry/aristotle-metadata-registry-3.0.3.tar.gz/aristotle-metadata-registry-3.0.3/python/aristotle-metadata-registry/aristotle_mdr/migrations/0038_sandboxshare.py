# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-22 02:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0037_make_name_shorttext'),
    ]

    operations = [
        migrations.CreateModel(
            name='SandboxShare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, editable=False, help_text='Universally-unique Identifier. Uses UUID1 as this improves uniqueness and tracking between registries', unique=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('emails', jsonfield.fields.JSONField()),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='share', to='aristotle_mdr.PossumProfile')),
            ],
        ),
    ]
