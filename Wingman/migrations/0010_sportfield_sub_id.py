# Generated by Django 3.1.7 on 2021-05-01 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wingman', '0009_auto_20210429_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportfield',
            name='sub_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
