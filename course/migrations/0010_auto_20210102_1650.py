# Generated by Django 2.1.5 on 2021-01-02 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20210102_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_class',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='course.Class'),
        ),
    ]
