# Generated by Django 3.0.9 on 2020-10-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videocourses', '0004_videocourse_allowed_memberships'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courselecture',
            name='video_link',
            field=models.FileField(upload_to=''),
        ),
    ]
