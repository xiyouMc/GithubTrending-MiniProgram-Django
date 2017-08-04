# coding:utf-8
import httplib
import urllib

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

#用户名是登录ihuyi.com账号名（例如：cf_demo123）
account = "C86355990"
#密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
password = "6c2aa1bd781974278c0d5df75eab6d9a"


def send_sms():
    params = urllib.urlencode({
        'account': account,
        'password': password,
        'content': "您的验证码是：11111。请不要把验证码泄露给其他人。",
        'mobile': "18758230408",
        'format': 'json'
    })
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn = httplib.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str