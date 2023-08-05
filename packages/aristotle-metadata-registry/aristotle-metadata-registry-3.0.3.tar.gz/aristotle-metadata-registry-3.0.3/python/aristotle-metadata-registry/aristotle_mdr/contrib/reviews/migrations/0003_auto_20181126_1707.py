# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 23:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aristotle_mdr_review_requests', '0002_auto_20181031_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewEndorsementTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('registration_state', models.IntegerField(choices=[(0, 'Not Progressed'), (1, 'Incomplete'), (2, 'Candidate'), (3, 'Recorded'), (4, 'Qualified'), (5, 'Standard'), (6, 'Preferred Standard'), (7, 'Superseded'), (8, 'Retired')], help_text='The state at which a user wishes a metadata item to be endorsed')),
                ('actor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ReviewStatusChangeTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Open'), (5, 'Revoked'), (10, 'Approved'), (15, 'Closed')], default=0, help_text='Status of a review')),
                ('actor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.RenameField(
            model_name='reviewrequest',
            old_name='state',
            new_name='target_registration_state',
        ),
        migrations.RenameField(
            model_name='reviewrequest',
            old_name='message',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='reviewrequest',
            name='status',
            field=models.IntegerField(choices=[(0, 'Open'), (5, 'Revoked'), (10, 'Approved'), (15, 'Closed')], default=0, help_text='Status of a review'),
        ),
        migrations.AddField(
            model_name='reviewstatuschangetimeline',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_changes', to='aristotle_mdr_review_requests.ReviewRequest'),
        ),
        migrations.AddField(
            model_name='reviewendorsementtimeline',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endorsements', to='aristotle_mdr_review_requests.ReviewRequest'),
        ),
    ]
