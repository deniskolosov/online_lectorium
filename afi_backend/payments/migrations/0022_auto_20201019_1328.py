# Generated by Django 3.0.9 on 2020-10-19 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0021_auto_20201019_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='payment_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yandex Checkout'), (1, 'Cloudpayments'), (2, 'PayPal'), (3, 'Alfa-Bank')], default=0, unique=True),
        ),
    ]
