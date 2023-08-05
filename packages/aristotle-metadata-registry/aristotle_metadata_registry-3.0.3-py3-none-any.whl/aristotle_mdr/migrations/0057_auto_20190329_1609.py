# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0056_auto_20190313_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationauthority',
            name='candidate',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Candidate' status level for this Registration Authority.", verbose_name='Candidate'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='incomplete',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Incomplete' status level for this Registration Authority.", verbose_name='Incomplete'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='locked_state',
            field=models.IntegerField(choices=[(0, 'Not Progressed'), (1, 'Incomplete'), (2, 'Candidate'), (3, 'Recorded'), (4, 'Qualified'), (5, 'Standard'), (6, 'Preferred Standard'), (7, 'Superseded'), (8, 'Retired')], default=2, help_text="When metadata is endorsed at  the specified 'locked' level, the metadata item will not longer be able to be altered by standard users. Only Workgroup or Organisation Stewards will be able to edit 'locked' metadata."),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='notprogressed',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Not Progressed' status level for this Registration Authority.", verbose_name='Not Progressed'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='preferred',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Preferred Standard' status level for this Registration Authority.", verbose_name='Preferred Standard'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='public_state',
            field=models.IntegerField(choices=[(0, 'Not Progressed'), (1, 'Incomplete'), (2, 'Candidate'), (3, 'Recorded'), (4, 'Qualified'), (5, 'Standard'), (6, 'Preferred Standard'), (7, 'Superseded'), (8, 'Retired')], default=3, help_text="When metadata is endorsed at the specified 'public' level, the metadata item will be visible to all users"),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='qualified',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Qualified' status level for this Registration Authority.", verbose_name='Qualified'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='recorded',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Recorded' status level for this Registration Authority.", verbose_name='Recorded'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='retired',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Retired' status level for this Registration Authority.", verbose_name='Retired'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='standard',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Standard' status level for this Registration Authority.", verbose_name='Standard'),
        ),
        migrations.AlterField(
            model_name='registrationauthority',
            name='superseded',
            field=models.TextField(blank=True, help_text="A description of the meaning of the 'Superseded' status level for this Registration Authority.", verbose_name='Superseded'),
        ),
    ]
