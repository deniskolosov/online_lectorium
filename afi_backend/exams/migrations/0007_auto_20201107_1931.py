# Generated by Django 3.0.9 on 2020-11-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0006_auto_20201107_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='chosen_answers',
            field=models.ManyToManyField(null=True, to='exams.Answer'),
        ),
    ]