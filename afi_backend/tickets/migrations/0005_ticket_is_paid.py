# Generated by Django 3.0.9 on 2020-10-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20200917_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
