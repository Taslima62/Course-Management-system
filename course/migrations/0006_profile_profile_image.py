# Generated by Django 2.1.5 on 2021-01-02 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_student_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='course/images/default-avatar.jpg', upload_to='course/images'),
        ),
    ]
