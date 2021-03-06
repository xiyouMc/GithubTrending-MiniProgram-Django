# -*- coding: utf-8 -*-
from django.http import HttpResponse
import requests
import json
import hashlib
import time
import xml.etree.ElementTree as ET
import wx_recevie as receive
import wx_reply as reply
from Instagram.models import Ins, WallPaper
import md5
import _redis
import base64

# https://www.instagram.com/stephencurry30
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
            print recMsg
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # replyMsg = reply.TextMsg(toUser, fromUser, 'avatar_name')
                # resultMsg= replyMsg.send()
                # return HttpResponse(replyMsg.send())
                if '壁纸' in recMsg.Content.strip() and 'instagram.com' in recMsg.Content.strip():
                    url = recMsg.Content.strip()[recMsg.Content.strip().find(
                        'http'):len(recMsg.Content.strip())]
                    print url
                    url = url + '?__a=1' + 'base64' + '0'
                    m = md5.new()
                    m.update(url)
                    str_md5 = m.hexdigest()

                    base64Data = _get_redis_task(url)
                    if base64Data is not None:
                        print 'sss'
                        savedBase64 = WallPaper.objects.filter(
                            md5=str_md5, index=0).exclude()
                        #存数据
                        if len(savedBase64) == 0:
                            wallpaper = WallPaper(
                                md5=str_md5,
                                url=url,
                                base64Str=json.loads(base64Data).get(
                                    'base64Str'),
                                index=0)
                            wallpaper.save()
                        wallInf = wallInfo(base64Data, toUser, fromUser,
                                           str_md5)
                        return HttpResponse(wallInf)

                    else:
                        js = {
                            'url':
                            recMsg.Content.strip()[recMsg.Content.strip().find(
                                'http'):len(recMsg.Content.strip())] +
                            '?__a=1',
                            'index':
                            0
                        }
                        _redis_push('base64', json.dumps(js))
                        startTime = time.time()
                        endTime = time.time()
                        while base64Data is None and (
                                endTime - startTime) < 8:
                            base64Data = _get_redis_task(url)
                            print base64Data
                            if base64Data is not None:
                                #存数据
                                savedBase64 = WallPaper.objects.filter(
                                    md5=str_md5, index=0).exclude()
                                if len(savedBase64) == 0:
                                    wallpaper = WallPaper(
                                        md5=str_md5,
                                        url=url,
                                        base64Str=json.loads(base64Data).get(
                                            'base64Str'),
                                        index=0)
                                    wallpaper.save()

                                wallInf = wallInfo(base64Data, toUser,
                                                   fromUser, str_md5)
                                return HttpResponse(wallInf)
                            endTime = time.time()

                elif 'instagram.com' in recMsg.Content.strip():
                    if '?' in recMsg.Content.strip() and recMsg.NeedAddWH.strip() == '1':
                        recMsg.Content = recMsg.Content.strip().split('?')[0]
                    # 保存数据库
                    m = md5.new()
                    m.update(recMsg.Content.strip())
                    str_md5 = m.hexdigest()
                    requestUrl = recMsg.Content.strip()
                    if recMsg.NeedAddWH.strip() == '1':
                        requestUrl = recMsg.Content.strip() + '?__a=1'
                    savedIns = Ins.objects.filter(md5=str_md5).exclude()
                    if len(savedIns) == 0:
                        ins = Ins(
                            md5=str_md5, url=base64.b64encode(requestUrl))
                        ins.save()

                    redisData = _get_redis_task(requestUrl)
                    if redisData is not None:
                        resultMsg = userInfo(redisData, toUser, fromUser,
                                             str_md5)
                        return HttpResponse(resultMsg)
                    else:
                        _redis_ = _redis.RedisC()
                        r = _redis_._redis_()
                        r.rpush('ins', requestUrl)
                        
                        redisData = None
                        startTime = time.time()
                        endTime = time.time()
                        while redisData == None and (endTime - startTime) < 8:
                            redisData = _get_redis_task(
                                requestUrl)
                            print redisData
                            if redisData is not None:
                                resultMsg = userInfo(redisData, toUser,
                                                     fromUser, str_md5)
                                return HttpResponse(resultMsg)
                            endTime = time.time()
                            # else:

                            #     resultMsg = "success"
                            #     return HttpResponse(resultMsg)
                elif '帮助' in recMsg.Content.strip() or  'help' in recMsg.Content.strip():
                    helpText = reply.TextMsg(toUser,fromUser,'<a href="https://python.0x2048.com/help/">insloader | 使用帮助</a >')
                    return HttpResponse(helpText.send())
                
                else:
                    print "暂且不处理"
                    helpText = reply.TextMsg(toUser,fromUser,'你貌似输错了。点击 https://python.0x2048.com/help/" |insloader | 使用帮助</a >')
                    return HttpResponse(helpText.send())
            elif isinstance(recMsg, receive.Event) and recMsg.MsgType == 'event':
                if recMsg.Event == 'subscribe':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    helpText = reply.TextMsg(toUser,fromUser,'insloader | 使用帮助 , 点击 https://python.0x2048.com/help/ 。在这里你可以保存 Ins 上的照片和视频，同时你也可以制作精美的壁纸。')
                    return HttpResponse(helpText.send())
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


def wallInfo(base64Data, toUser, fromUser, _md5):
    return base64Data
    # picUrl = json.loads(base64Data).get('picUrl')
    # replyImgMsg = reply.ImgText(
    #     toUser, fromUser, 'WallPaper', picUrl,
    #     'https://python.0x2048.com/wallpaper/?md5Str=' + _md5 + "&index=0")

    # result = replyImgMsg.send()
    # # print result
    # # replyMsg = reply.TextMsg(toUser, fromUser, avatar_name)
    # return result


def userInfo(redisData, toUser, fromUser, _md5):
    js = json.loads(redisData)
    return redisData
    # avatar_url = js.get('avatar_url')
    # avatar_href = js.get('avatar_href')
    # avatar_name = js.get('avatar_name')

    # replyImgMsg = reply.ImgText(toUser, fromUser, avatar_name, avatar_url,
    #                             'https://python.0x2048.com/q/?md5Str=' + _md5)

    # result = replyImgMsg.send()
    # # print result
    # # replyMsg = reply.TextMsg(toUser, fromUser, avatar_name)
    # return result


def _get_redis_task(key):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    return r.get(key)


def _redis_push(key, values):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    return r.rpush(key, values)
