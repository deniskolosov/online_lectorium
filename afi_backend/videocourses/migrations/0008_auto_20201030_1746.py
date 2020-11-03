# Generated by Django 3.0.9 on 2020-10-30 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videocourses', '0007_auto_20201016_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoCoursePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='videocourses.VideoCourse')),
            ],
        ),
        migrations.AddField(
            model_name='courselecture',
            name='part',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='videocourses.VideoCoursePart'),
        ),
    ]