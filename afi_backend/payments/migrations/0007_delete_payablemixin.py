# Generated by Django 3.0.9 on 2020-09-15 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20200915_1526'),
        ('payments', '0006_payablemixin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PayableMixin',
        ),
    ]
