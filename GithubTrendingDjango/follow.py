from django.http import HttpResponse
import requests
from github_utils import read_cookies, get_auth_token
import re


def GithubFollow(request):
    if 'to_user' in request.GET:
        to_user = request.GET['to_user']
        print request.GET
        username = request.GET['username']
        follow_resule = Follow(to_user, username)
        return HttpResponse(follow_resule)


def Follow(to_user, username):
    s = requests.Session()
    s.cookies = read_cookies(username)
    star = s.get('https://github.com/' + to_user, verify=False)
    # return star.text
    auto_token_content = re.findall('users/follow(.*?)</div>', star.text)
    print auto_token_content
    print auto_token_content
    data = {
        'utf8': '%E2%9C%93',
        'authenticity_token': get_auth_token(auto_token_content[0])
    }
    s.headers.update({'X-Requested-With': 'XMLHttpRequest'})
    follow_result = s.post(
        'https://github.com/users/follow?target=' + to_user,
        data=data,
        verify=False)
    return follow_result.text