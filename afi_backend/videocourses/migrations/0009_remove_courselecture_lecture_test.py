# Generated by Django 3.0.9 on 2020-11-05 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videocourses', '0008_auto_20201030_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courselecture',
            name='lecture_test',
        ),
    ]
