# Generated by Django 4.2.7 on 2023-11-23 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_post_comments_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
