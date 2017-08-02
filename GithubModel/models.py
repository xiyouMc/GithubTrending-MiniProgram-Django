# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)


class Search(models.Model):
    username = models.CharField(max_length=20)
    search = models.CharField(max_length=20)
    date = models.DateTimeField('查询时间', auto_now=True)
