# -*- coding: utf-8 -*-
from django.http import HttpResponse
import requests
import json
import hashlib
import time
import xml.etree.ElementTree as ET
import wx_recevie as receive
import wx_reply as reply
from Instagram.models import Ins
import md5
import _redis


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
            recMsg = receive.parse_xml(request.body)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # replyMsg = reply.TextMsg(toUser, fromUser, 'avatar_name')
                # resultMsg= replyMsg.send()
                # return HttpResponse(replyMsg.send())

                if 'instagram.com' in recMsg.Content:
                    # 保存数据库
                    m = md5.new()
                    m.update(recMsg.Content)
                    str_md5 = m.hexdigest()
                    savedIns = Ins.objects.filter(md5=str_md5).exclude()
                    if len(savedIns) == 0:
                        ins = Ins(md5=str_md5, url=recMsg.Content + '?__a=1')
                        ins.save()

                    redisData = _get_redis_task(recMsg.Content + '?__a=1')
                    if redisData is not None:
                        resultMsg = userInfo(redisData, toUser, fromUser,
                                             str_md5)
                        return HttpResponse(resultMsg)
                    else:
                        _redis_ = _redis.RedisC()
                        r = _redis_._redis_()
                        r.rpush('ins', recMsg.Content + '?__a=1')
                        redisData = None
                        while redisData == None:
                            redisData = _get_redis_task(
                                recMsg.Content + '?__a=1')
                            print redisData
                            if redisData is not None:
                                resultMsg = userInfo(redisData, toUser,
                                                     fromUser, str_md5)
                                return HttpResponse(resultMsg)
                            # else:
                            #     resultMsg = "success"
                            #     return HttpResponse(resultMsg)
                else:
                    print "暂且不处理"
                    resultMsg = "success"
                    return HttpResponse(resultMsg)
            else:
                print "暂且不处理"
                resultMsg = "success"
                # return HttpResponse(resultMsg)

            return HttpResponse(resultMsg)
    except Exception, Argument:
        a = {"errorcode": '-2'}
        print Argument
        return HttpResponse(json.dumps(a))


def userInfo(redisData, toUser, fromUser, _md5):
    print redisData
    js = json.loads(redisData)
    avatar_url = js.get('graphql').get('shortcode_media').get('owner').get(
        'profile_pic_url')
    avatar_href = 'https://www.instagram.com/%s/' % js.get('graphql').get(
        'shortcode_media').get('owner').get('username')
    avatar_name = js.get('graphql').get('shortcode_media').get('owner').get(
        'username')

    replyImgMsg = reply.ImgText(toUser, fromUser, avatar_name, avatar_url,
                                'https://python.0x2048.com/q/?md5Str=' + _md5)

    result = replyImgMsg.send()
    # print result
    # replyMsg = reply.TextMsg(toUser, fromUser, avatar_name)
    return result


def _get_redis_task(key):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    return r.get(key)