# Generated by Django 2.1.5 on 2021-06-15 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0030_auto_20210615_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='vote',
            field=models.FloatField(default=-1.0),
        ),
    ]
