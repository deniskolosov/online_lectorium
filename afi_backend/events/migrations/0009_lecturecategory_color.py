# Generated by Django 3.0.9 on 2020-09-17 11:36

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20200916_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturecategory',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True),
        ),
    ]
