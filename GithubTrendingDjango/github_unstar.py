from django.http import HttpResponse
from github_utils import read_cookies, get_auth_token
import requests
import re


def GithubUnStar(request):
    if 'github' in request.GET:
        s = requests.Session()
        repo = request.GET['github']
        username = request.GET['username']
        s.cookies = read_cookies(username)
        star = s.get('https://github.com/' + repo, verify=False)
        auto_token_content = re.findall(repo + '/star"(.*?)</div>', star.text)
        print auto_token_content
        data = {
            'utf8': '%E2%9C%93',
            'authenticity_token': get_auth_token(auto_token_content[0])
        }
        s.headers.update({'X-Requested-With': 'XMLHttpRequest'})
        star_re = s.post(
            'https://github.com/' + repo + '/unstar', data=data, verify=False)
        return HttpResponse(star_re.text)