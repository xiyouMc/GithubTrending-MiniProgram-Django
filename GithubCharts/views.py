# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from highcharts.views import HighChartsBarView
from django.shortcuts import render
from GithubModel import models


# Create your views here.
class SearchView(HighChartsBarView):
    l = models.Search.objects.all()