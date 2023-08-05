# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 03:21
from __future__ import unicode_literals

from django.db import migrations, models


def move_slot_info(apps, schema_editor):
    Slot = apps.get_model('aristotle_mdr_slots', 'slot')

    for slot in Slot.objects.all():
        slot.name = slot.type.slot_name
        slot.new_type = slot.type.datatype
        slot.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr_slots', '0002_lengthen_slot_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='name',
            field=models.CharField(default='Slot name lost during migration', max_length=256, blank=True),
            preserve_default=False,
        ),

        migrations.RunPython(move_slot_info, reverse_code=migrations.RunPython.noop),

        migrations.AddField(
            model_name='slot',
            name='new_type',
            field=models.CharField(max_length=256, blank=True),
        ),

        migrations.RemoveField(
            model_name='slotdefinition',
            name='datatype',
        ),

        migrations.RemoveField(
            model_name='slot',
            name='type',
        ),

        migrations.RenameField(
            model_name='slot',
            old_name='new_type',
            new_name='type',
        ),

        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(max_length=256),
            preserve_default=False,
        ),

        migrations.DeleteModel(
            name='SlotDefinition',
        ),
    ]
