# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-27 11:49
from __future__ import unicode_literals

import aristotle_mdr.fields
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comet', '0010_auto_20190417_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrameworkDimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=2048)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='framework',
            name='indicators',
        ),
        migrations.RemoveField(
            model_name='framework',
            name='parentFramework',
        ),
        migrations.AddField(
            model_name='indicator',
            name='quality_statement',
            field=aristotle_mdr.fields.ConceptForeignKey(blank=True, help_text='A statement of multiple quality dimensions for the purpose of assessing the quality of the data for reporting against this Indicator.', null=True, on_delete=django.db.models.deletion.CASCADE, to='comet.QualityStatement'),
        ),
        migrations.AddField(
            model_name='frameworkdimension',
            name='framework',
            field=aristotle_mdr.fields.ConceptForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet.Framework'),
        ),
        migrations.AddField(
            model_name='frameworkdimension',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_dimensions', to='comet.FrameworkDimension'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='dimensions',
            field=aristotle_mdr.fields.ConceptManyToManyField(blank=True, related_name='indicators', to='comet.FrameworkDimension'),
        ),
    ]
