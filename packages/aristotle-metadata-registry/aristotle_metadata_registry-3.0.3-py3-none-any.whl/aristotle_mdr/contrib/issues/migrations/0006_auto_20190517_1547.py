# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 05:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0062_auto_20190517_1016'),
        ('aristotle_mdr_issues', '0005_auto_20190514_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('stewardship_organisation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='aristotle_mdr.StewardOrganisation', to_field='uuid')),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, to='aristotle_mdr_issues.IssueLabel'),
        ),
    ]
