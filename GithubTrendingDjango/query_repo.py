from django.http import HttpResponse
import hashlib
import requests
import json
import settings
import os
from util import _get_time


def GithubRepo(request):
    if 'github' in request.GET:
        github_url = request.GET['github']
        m2 = hashlib.md5()
        m2.update(github_url)
        url_md5 = m2.hexdigest()
        if os.path.exists(settings.dirs + '/' + _get_time() + url_md5):
            with open(settings.dirs + '/' + _get_time() + url_md5, 'r') as f:
                c = f.readline()
        _json = requests.get(github_url, verify=False, headers=settings.header)
        if (_json):
            _json_data = json.loads(_json.text)
            for j in _json_data:
                print j
                n = j['name'].lower()
                print n
                if n == 'readme.md':
                    github_url += j['path']
                    _json = requests.get(github_url, verify=False)
                    break
        with open(settings.dirs + '/' + _get_time() + url_md5, 'w') as f:
            f.write(_json.text.encode('utf-8'))
        return HttpResponse(_json.text)
