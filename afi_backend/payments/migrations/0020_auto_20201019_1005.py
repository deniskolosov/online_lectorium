# Generated by Django 3.0.9 on 2020-10-19 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0019_subscription_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.PaymentMethod'),
        ),
    ]
