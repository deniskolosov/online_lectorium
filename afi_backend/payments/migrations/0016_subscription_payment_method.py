# Generated by Django 3.0.9 on 2020-10-15 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0015_auto_20201015_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='payment_method',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='payments.PaymentMethod'),
        ),
    ]
