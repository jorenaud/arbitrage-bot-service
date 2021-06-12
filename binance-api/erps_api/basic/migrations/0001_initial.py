# Generated by Django 2.2.7 on 2020-06-05 14:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='access_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_addr', models.CharField(max_length=255)),
                ('serverName', models.CharField(default='', max_length=200)),
                ('tradeType', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='adminemails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailType', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=200)),
                ('password', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=200)),
                ('currency', models.CharField(default='', max_length=200)),
                ('intervalId', models.IntegerField(default=0)),
                ('priceId', models.IntegerField(default=0)),
                ('period', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='botList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(default='', max_length=200)),
                ('botID', models.IntegerField(default=0)),
                ('quantity', models.FloatField(default=0.0)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='cmenu_tree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.IntegerField(default=0)),
                ('has_child', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='event_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('result', models.CharField(max_length=255)),
                ('part', models.CharField(max_length=255)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip_addr', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='interval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='menu_tree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.IntegerField(default=0)),
                ('has_child', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='news',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=20000)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.IntegerField(default=0)),
                ('orderId', models.IntegerField(default=0)),
                ('currency', models.CharField(default='', max_length=200)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('size', models.FloatField(default=0.0)),
                ('price', models.FloatField(default=0.0)),
                ('commission', models.FloatField(default=0.0)),
                ('side', models.CharField(default='', max_length=200)),
                ('orderType', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('duration', models.IntegerField(default=7)),
                ('description', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='privilege',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='', max_length=100)),
                ('lastName', models.CharField(default='', max_length=100)),
                ('userName', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(default=None, max_length=254)),
                ('phone', models.CharField(default='', max_length=200)),
                ('password', models.CharField(default='', max_length=400)),
                ('country', models.CharField(default='', max_length=100)),
                ('language', models.CharField(default='', max_length=100)),
                ('status', models.IntegerField(default=0)),
                ('balance', models.CharField(default='', max_length=1000000)),
                ('apiKey', models.CharField(default='', max_length=500)),
                ('apiSecret', models.CharField(default='', max_length=500)),
                ('role', models.IntegerField(default=0)),
                ('planId', models.IntegerField(default=0)),
                ('regTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('expireTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('verify', models.BooleanField(default=True)),
            ],
        ),
    ]
