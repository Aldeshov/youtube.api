# Generated by Django 3.2 on 2021-05-14 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0003_channel_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='channel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subscribed',
            field=models.ManyToManyField(blank=True, related_name='channel_subscribers', to='applications.Channel'),
        ),
    ]