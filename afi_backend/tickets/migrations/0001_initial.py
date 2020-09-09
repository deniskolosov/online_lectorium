# Generated by Django 3.0.9 on 2020-09-09 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scanned', models.BooleanField(default=False)),
                ('ticket', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket')),
            ],
        ),
    ]
