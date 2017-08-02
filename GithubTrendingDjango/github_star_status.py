from django.http import HttpResponse
import requests
import json
from github_utils import read_cookies
import threading
import re


class ResponseStar:
    def __init__(self):
        self.repo = ''
        self.stared = ''


class Model:
    def __init__(self):
        self.s = requests.Session()
        self._repos = []
        self.repo_size = 0


def GithubStarStatus(request):
    if 'githubs' in request.GET:
        model = Model()
        repos = request.GET['githubs']
        repos = repos.replace('&quot;', '"')
        _json_repos = json.loads(repos)
        username = request.GET['username']
        model.s.cookies = read_cookies(username)
        threads = []
        model.repo_size = len(_json_repos)
        for repo in _json_repos:
            t = threading.Thread(target=status, args=(repo, model))
            threads.append(t)
        for t in threads:
            t.setDaemon(True)
            t.start()
        while model.repo_size is not 0:
            pass
        _json_resp = json.dumps(model._repos)
        return HttpResponse(_json_resp)


def status(repo, model):
    repo_content = model.s.get('https://github.com/' + repo, verify=False)
    is_star = re.findall('starring-container on', repo_content.text)
    print is_star
    if not is_star:
        stared = 'not_star'
    else:
        stared = 'stared'
    responseStared = ResponseStar()
    responseStared.repo = repo
    responseStared.stared = stared
    model._repos.append(responseStared.__dict__)
    model.repo_size = model.repo_size - 1
