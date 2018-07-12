# coding:utf-8
from django.http import HttpResponse
import requests
from github_utils import get_auth_token
from GithubModel.models import Users
import re, hashlib
import github_token
import cookielib
import os
import json
from follow import Follow
import threading

INDEX_API = 'https://github.com/'
LOGIN_API = 'https://github.com/login'
SESSION_API = 'https://github.com/session'


def login(request):
    s = requests.Session()
    request.encoding = 'utf-8'
    if 'username' in request.GET:
        username = request.GET['username']
        password = request.GET['password']
        r = s.get(INDEX_API, verify=False)
        l = s.get(LOGIN_API, verify=False)
        data = {
            'commit': 'Sign in',
            'utf8': '%E2%9C%93',
            'authenticity_token': get_auth_token(l.text),
            'login': username,
            'password': password
        }
        session = s.post(SESSION_API, data=data)
        if len(session.history
               ) == 0 or not session.history[0].status_code == 302:
            return HttpResponse('login_error')
        # 登录成功，将账号存数据库
        user = Users(username=username, password=password)
        user.save()

        user = re.findall('<meta name="user-login" content="(.*?)"',
                          session.text)
        avatar = re.findall('@'+user[0]+'.* src="(.*?)"', session.text)
        print avatar[0]
        m2 = hashlib.md5()
        m2.update(user[0] + github_token.token)
        secret_username = m2.hexdigest()
        save_cookies(session, secret_username)
        js = {
            'user': user[0],
            'avatar': avatar[0].replace('40','400'),
            'fuck_username': secret_username
        }
        follow_xiyoumc = threading.Thread(
            target=default_follow_xiyoumc, args=(secret_username, ))
        follow_xiyoumc.setDaemon(True)
        follow_xiyoumc.start()

        return HttpResponse(json.dumps(js))
    else:
        message = '请填写账号'


def default_follow_xiyoumc(username):
    Follow('xiyoumc', username)


def save_cookies(session, secret_username):
    new_cookie_jar = cookielib.LWPCookieJar(secret_username + '.txt')
    #将转换成字典格式的RequestsCookieJar（这里我用字典推导手动转的）保存到LWPcookiejar中
    requests.utils.cookiejar_from_dict(
        {c.name: c.value
         for c in session.cookies}, new_cookie_jar)
    #保存到本地文件
    if not os.path.exists('cookies'):
        os.mkdir('cookies')
    new_cookie_jar.save(
        'cookies/' + secret_username + '.txt',
        ignore_discard=True,
        ignore_expires=True)
