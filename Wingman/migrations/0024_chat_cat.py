# Generated by Django 3.1.7 on 2021-05-02 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wingman', '0023_auto_20210502_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat_Cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
    ]
