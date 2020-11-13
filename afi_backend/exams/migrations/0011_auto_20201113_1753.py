# Generated by Django 3.0.9 on 2020-11-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('exams', '0010_remove_exam_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testassignment',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'events'), ('model', 'videolecture')), models.Q(('app_label', 'videocourses'), ('model', 'videocoursepart')), models.Q(('app_label', 'events'), ('model', 'courselecture')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
