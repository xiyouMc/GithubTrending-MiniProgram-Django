# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Ins(models.Model):
    md5 = models.CharField(max_length=100)
    url = models.CharField(max_length=100)