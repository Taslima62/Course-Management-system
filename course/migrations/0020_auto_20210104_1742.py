# Generated by Django 2.1.5 on 2021-01-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_auto_20210104_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(upload_to='course/images/'),
        ),
    ]
