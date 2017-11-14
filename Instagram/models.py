# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Ins(models.Model):
    md5 = models.CharField(max_length=100)
    url = models.CharField(max_length=100)


class WallPaper(models.Model):
    md5 = models.CharField(max_length=100)
    # bgc = models.CharField(max_length=10)
    # radius = models.CharField(max_length=10)
    # location = models.CharField(max_length=10)
    index = models.IntegerField(default=0)
    url = models.CharField(max_length=100)
    base64Str = models.TextField(blank=True, null=True)
