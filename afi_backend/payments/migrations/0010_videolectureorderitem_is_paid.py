# Generated by Django 3.0.9 on 2020-10-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20201002_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='videolectureorderitem',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
