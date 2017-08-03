# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django.utils.timezone as timezone
from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)


class Search(models.Model):
    username = models.CharField(max_length=20)
    search = models.CharField(max_length=20)
    date = models.DateTimeField('查询时间', default = timezone.now)


class IP(models.Model):
    ip = models.CharField(max_length=20)
    data = models.DateTimeField('当前时间', default = timezone.now)
