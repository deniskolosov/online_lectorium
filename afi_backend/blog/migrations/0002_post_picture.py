# Generated by Django 3.0.9 on 2020-10-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(null=True, upload_to='blog_pictures/'),
        ),
    ]
