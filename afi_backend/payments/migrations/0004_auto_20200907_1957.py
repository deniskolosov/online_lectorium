# Generated by Django 3.0.9 on 2020-09-07 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('payments', '0003_payment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_for',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
