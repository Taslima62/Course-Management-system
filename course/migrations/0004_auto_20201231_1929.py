# Generated by Django 2.1.5 on 2020-12-31 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_class_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='code',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
    ]
