# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-14 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instagram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WallPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('base64Str', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
