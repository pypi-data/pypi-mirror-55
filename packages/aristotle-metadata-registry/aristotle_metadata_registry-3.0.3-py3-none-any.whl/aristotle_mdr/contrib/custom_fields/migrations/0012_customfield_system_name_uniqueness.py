# Generated by Django 2.2.5 on 2019-09-11 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr_custom_fields', '0011_customfield_generate_system_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfield',
            name='system_name',
            field=models.CharField(default='',
                                   help_text='A name used for uniquely identifying the custom field',
                                   max_length=1000,
                                   unique=True),
        ),
    ]
