# Generated by Django 3.0.9 on 2020-10-29 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_videolecture_allowed_memberships'),
        ('blog', '0002_post_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Category'),
        ),
    ]
