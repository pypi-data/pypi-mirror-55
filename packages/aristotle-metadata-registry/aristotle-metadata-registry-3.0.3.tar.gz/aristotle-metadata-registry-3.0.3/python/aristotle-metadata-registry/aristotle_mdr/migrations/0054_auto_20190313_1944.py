# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-13 08:44
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aristotle_mdr', '0053_auto_20190226_0536'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkgroupMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('manager', 'Manager'), ('steward', 'Steward'), ('submitters', 'Submitter'), ('viewer', 'Viewer')], help_text='Role within this group', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='workgroup',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, null=True, editable=True, populate_from='name', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workgroup',
            name='state',
            field=models.CharField(choices=[('active', 'Active'), ('archived', 'Deactivated & Visible'), ('hidden', 'Deactivated & Hidden')], default='active', help_text='Status of this group', max_length=128),
        ),
        migrations.AlterField(
            model_name='workgroup',
            name='name',
            field=models.TextField(help_text='The primary name used for human identification purposes.'),
        ),
        migrations.AlterField(
            model_name='workgroup',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid1, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='workgroupmembership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='aristotle_mdr.Workgroup', to_field='uuid'),
        ),
        migrations.AddField(
            model_name='workgroupmembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='workgroupmembership',
            unique_together=set([('user', 'group')]),
        ),
    ]
