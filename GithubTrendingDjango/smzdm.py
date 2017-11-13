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
            toUserName = body.get('ToUserName')
            msgType = body.get('MsgType')
            print fromUserName,fromUserName,msgType
            js = {
                'fromUserName': 'fromUserName',
                'createTime': 'createTime',
                'msgType': 'msgType'
            }
            if msgType == 'text':
                content = 'test'
                replyMsg = TextMsg(toUserName,fromUserName,content)
            print replyMsg.send()
            return HttpResponse(replyMsg.send())
    except Exception, Argument:
        a = {"errorcode": '-2'}
        return HttpResponse(json.dumps(a))


class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        print XmlForm
        return XmlForm.format(**self.__dict)

# def message(request):
#     try:
