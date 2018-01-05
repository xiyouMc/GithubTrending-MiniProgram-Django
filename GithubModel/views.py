# coding:utf-8
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
import json

# Create your views here.
d = {
    '1.htldxhzj.duapp.com': 9398,
    'gtxapi.cdn.duapp.com': 79496,
    'www.xxx.com': 2477070,
    'www.baidu.com': 1465,
    'www.bing.com': 777,
    'www.aaa.com': 1113101,
    'www.ccc.net.cn': 922,
    'www.zhanimei.ga': 29847,
    'www.zhanimei.ml': 40155,
    'www.zhasini.ml': 373436
}


def index(request):
    categories = d.keys()
    print categories
    data = d.values()
    return render_to_response('github/index.html', {
        'user': request.user,
        'categories': categories,
        'data': data
    })

def alipay(request):
    return render_to_response('github/alipay.html')

def ys(request):
    return render_to_response('github/ys.html')