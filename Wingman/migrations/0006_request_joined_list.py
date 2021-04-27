# Generated by Django 3.1.7 on 2021-04-27 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Wingman', '0005_auto_20210427_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_Joined_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_joined_lists', to='Wingman.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_joined_lists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]