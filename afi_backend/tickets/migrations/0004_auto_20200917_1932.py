# Generated by Django 3.0.9 on 2020-09-17 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_offlinelecture_capacity'),
        ('tickets', '0003_auto_20200915_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='offline_lecture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.OfflineLecture'),
        ),
    ]
