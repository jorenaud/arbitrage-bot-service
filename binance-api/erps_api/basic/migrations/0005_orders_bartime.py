# Generated by Django 2.2.7 on 2020-06-13 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_bot_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='barTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]