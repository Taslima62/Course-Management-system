# Generated by Django 2.1.5 on 2021-01-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20210103_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='', upload_to='course/images/'),
        ),
    ]
