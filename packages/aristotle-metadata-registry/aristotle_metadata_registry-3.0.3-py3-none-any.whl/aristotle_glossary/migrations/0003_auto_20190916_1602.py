# Generated by Django 2.2.4 on 2019-09-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_glossary', '0002_auto_20190809_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryitem',
            name='index',
            field=models.ManyToManyField(blank=True, related_name='related_glossary_items', to='aristotle_mdr._concept'),
        ),
    ]
