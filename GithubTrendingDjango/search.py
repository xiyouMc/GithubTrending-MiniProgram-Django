from django.http import HttpResponse
import requests
import urllib
from settings import SEARCH_API, header
from GithubModel.models import Search


def GithubSearch(request):
    if 'q' in request.GET:
        q = request.GET['q']
        username = request.GET.get('username')
        if username is None:
            username = ''
        se = Search(search=q, username=username)
        se.save()
        q = urllib.quote(str(q))
        api = SEARCH_API % q
        r = requests.get(api, headers=header, verify=False)
        return HttpResponse(r.text)