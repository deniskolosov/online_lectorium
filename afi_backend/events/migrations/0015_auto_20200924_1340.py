# Generated by Django 3.0.9 on 2020-09-24 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0014_onlinelecturebulletpoint_videolecture_videolecturecertificate'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersVideoLectureCertificates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VideoLectureBulletPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('text_ru', models.TextField(null=True)),
                ('text_en', models.TextField(null=True)),
                ('video_lecture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bullet_points', to='events.VideoLecture')),
            ],
        ),
        migrations.RemoveField(
            model_name='videolecturecertificate',
            name='given_to',
        ),
        migrations.DeleteModel(
            name='OnlineLectureBulletPoint',
        ),
        migrations.AddField(
            model_name='usersvideolecturecertificates',
            name='certificate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.VideoLectureCertificate'),
        ),
        migrations.AddField(
            model_name='usersvideolecturecertificates',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]