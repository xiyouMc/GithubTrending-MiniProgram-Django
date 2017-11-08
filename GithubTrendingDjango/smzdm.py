from django.http import HttpResponse
import requests
import json
import hashlib


def Coupon(request):
    try:
        print request.method
        if request.method == 'GET':
            signature = request.GET.get('signature')
            timestamp = request.GET.get('timestamp')
            nonce = request.GET.get('nonce')
            echostr = request.GET.get('echostr')
            token = "smzdm1234"
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return HttpResponse(echostr)
            else:
                a = {"errorcode": '-1'}
                return HttpResponse(a)
        elif request.method == 'POST':
            print dir(request.body)
            body = json.loads(request.body)
            fromUserName = body.get('FromUserName')
            createTime = body.get('CreateTime')
            msgType = body.get('MsgType')
            print fromUserName,fromUserName,msgType
            js = {
                'fromUserName': 'fromUserName',
                'createTime': 'createTime',
                'msgType': 'msgType'
            }
            return HttpResponse(json.dumps(js))
    except Exception, Argument:
        a = {"errorcode": '-2'}
        return HttpResponse(json.dumps(a))


# def message(request):
#     try:
