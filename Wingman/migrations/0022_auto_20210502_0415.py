# Generated by Django 3.1.7 on 2021-05-01 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wingman', '0021_auto_20210502_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='bringup_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
