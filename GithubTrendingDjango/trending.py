# coding:utf-8
from django.http import HttpResponse
import requests
import urllib
import settings
import os
import util


def Trending(request):
    if 'since' in request.GET:
        if not os.path.exists(settings.dirs):
            os.mkdir(settings.dirs)
        since = request.GET['since']
        language = request.GET.get('language')
        if language is not None:
            language = urllib.quote(language)
            filename = util._get_time() + since + language + '.json'
        else:
            filename = util._get_time() + since + '.json'
        # 查找是否已经请求过
        local_path = settings.dirs + '/' + filename
        if os.path.exists(local_path):
            with open(local_path, 'r') as file:
                content = file.readline()
            if content is not '':
                return HttpResponse(content)
        if language is not None:
            trending_api = settings.CODEHUB_API_LAN % (since, language)
        else:
            trending_api = settings.CODEHUB_API % since
        _trending_json = requests.get(trending_api)
        with open(local_path, 'w') as f:
            f.write(_trending_json.text.encode('utf-8'))
        return HttpResponse(_trending_json.text)
