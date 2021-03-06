# Generated by Django 3.1.7 on 2021-05-01 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Wingman', '0018_user_comment_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_comment',
            old_name='user',
            new_name='poster',
        ),
        migrations.AddField(
            model_name='user_comment',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
