# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from models import Ins, WallPaper
import requests
from GithubTrendingDjango import _redis
import time

class ConfigObj(object):
    def __init__(self):
        self.isShowIns = False
def Config(request):
    config = ConfigObj()
    return HttpResponse(json.dumps(config.__dict__))

def help(request):
    return render_to_response('ins/help.html',{})

def imgToBase64(request):
    imgUrl = request.GET['imgUrl']
    imgBase64 = _get_redis_task(imgUrl)
    if imgBase64 is not None:
        return HttpResponse(imgBase64,mimetype="text/plain")
    else:
        _redis_push('imgToBase64', imgUrl)
        imgBase64 = None
        startTime = time.time()
        endTime = time.time()
        while imgBase64 is None and (endTime - startTime) < 15:
            imgBase64 = _get_redis_task(imgUrl)
            print imgBase64
            if imgBase64 is not None:
                return HttpResponse(imgBase64)
            endTime = time.time()


def wallpaper(request):
    print request.GET['md5Str']
    md5Str = request.GET['md5Str']
    index = request.GET['index']
    # bgc = request.GET['bgc']
    # radius = request.GET['radius']
    # location = request.GET['location']
    a = WallPaper.objects.filter(md5=md5Str, index=index).exclude()
    if len(a) > 0:
        # print a[0].base64Str
        base64Str = a[0].base64Str
        return render_to_response('ins/wallpaper.html',
                                  {'base64Str': base64Str,
                                   'md5Str': md5Str})
    else:
        url = request.GET['url']
        key = url + 'base64' + str(index)
        js = {'url': url, 'index': index}
        _redis_push('base64', json.dumps(js))
        print key
        base64Data = _get_redis_task(key)
        print base64Data
        if base64Data is not None:
            #存数据
            savedBase64 = WallPaper.objects.filter(
                md5=md5Str, index=index).exclude()
            if len(savedBase64) == 0:
                wallpaper = WallPaper(
                    md5=md5Str,
                    url=url,
                    base64Str=json.loads(base64Data).get('base64Str'),
                    index=index)
                wallpaper.save()
            print 'base64Data'
            print base64Data
            print md5Str
            return render_to_response('ins/wallpaper.html', {
                'base64Str':
                json.loads(base64Data).get('base64Str'),
                'md5Str':
                md5Str
            })
        else:
            while base64Data is None:
                base64Data = _get_redis_task(key)
                if base64Data is not None:
                    #存数据
                    savedBase64 = WallPaper.objects.filter(
                        md5=md5Str, index=index).exclude()
                    if len(savedBase64) == 0:
                        wallpaper = WallPaper(
                            md5=md5Str,
                            url=url,
                            base64Str=json.loads(base64Data).get('base64Str'),
                            index=index)
                        wallpaper.save()
                    print 'base64Data'
                    print base64Data
                    print md5Str
                    return render_to_response('ins/wallpaper.html', {
                        'base64Str':
                        json.loads(base64Data).get('base64Str'),
                        'md5Str':
                        md5Str
                    })


def _redis_push(key, values):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    return r.rpush(key, values)


def getOriginData(request):
    url = request.GET['url']
    print url
    redisData = _get_redis_task(url)
    isVideo = 'mp4' in url
    isImage = 'png' or 'jpg' or 'jpeg' in url
    print redisData
    if redisData is not None:
        contentType = ''
        if isVideo:
            contentType = 'video/mp4'
        elif isImage:
            contentType = 'image/jpeg'
        return HttpResponse(redisData,content_type=contentType)
    else:
        # _write_redis_status('ins',url)
        r.rpush('ins', url)
        redisData = None
        # print  _get_redis_task(url)
        while redisData == None:
            redisData = _get_redis_task(url)
            print redisData
            if redisData is not None:
                contentType = ''
                if isVideo:
                    contentType = 'video/mp4'
                elif isImage:
                    contentType = 'image/jpeg'
                return HttpResponse(redisData,content_type=contentType)

# Create your views here.
def q(request):
    # print request.get('md5Str')
    print request.GET['md5Str']
    _md5 = request.GET['md5Str']

    a = Ins.objects.filter(md5=_md5).exclude()
    if len(a) > 0:
        print a[0].url
        url = a[0].url

    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    print url
    redisData = _get_redis_task(url)
    print redisData
    if redisData is not None:
        return render(redisData, _md5, url)
    else:
        # _write_redis_status('ins',url)
        r.rpush('ins', url)
        redisData = None
        # print  _get_redis_task(url)
        while redisData == None:
            redisData = _get_redis_task(url)
            print redisData
            if redisData is not None:
                return render(redisData, _md5, url)
        # s = requests.get(url,verify=False)


def render(redisData, _md5, url):
    js = json.loads(redisData)
    # avatar_url = js.get('graphql').get('shortcode_media').get('owner').get(
    #     'profile_pic_url')
    # avatar_href = 'https://www.instagram.com/%s/' % js.get('graphql').get(
    #     'shortcode_media').get('owner').get('username')
    # avatar_name = js.get('graphql').get('shortcode_media').get('owner').get(
    #     'username')
    # edge_sidecar_to_children = js.get('graphql').get('shortcode_media').get(
    #     'edge_sidecar_to_children')
    # if edge_sidecar_to_children == None:
    #     display_resources = js.get('graphql').get('shortcode_media').get(
    #         'display_resources')
    # imgs = []
    # if edge_sidecar_to_children:
    #     edges = edge_sidecar_to_children.get('edges')
    #     for edge in edges:
    #         node = edge.get('node')
    #         display_resources = node.get('display_resources')
    #         img = display_resources[len(display_resources) - 1].get('src')
    #         imgs.append(img)
    # else:
    #     imgs.append(display_resources[len(display_resources) - 1].get('src'))
    isVideo = js.get('isVideo')
    if not isVideo:
        avatar_name = js.get('avatar_name')
        avatar_url = js.get('avatar_url')
        avatar_href = js.get('avatar_href')
        imgs = js.get('imgsBase64')
        createTime = js.get('createTime')
        shortcode = js.get('shortcode')
        index = 0
        jump_urls = []
        # for img in imgs:
        #     jump_urls.append('https://python.0x2048.com/wallpaper/?md5Str=' + _md5
        #                      + "&index=" + str(index))
        #     index = index + 1

        # print a.url
        return render_to_response('ins/index.html', {
            'avatar_name': avatar_name,
            'avatar_url': avatar_url,
            'avatar_href': avatar_href,
            'imgs': imgs,
            'md5': _md5,
            'url': url,
            'nums': range(len(imgs)),
            'createTime': createTime,
            'shortcode': shortcode
        })
    else:
        videoUrl = js.get('videoUrl')
        jpgUrl = js.get('jpgUrl')
        desc = js.get('desc')
        avatar_url = js.get('avatar_url')
        avatar_href = js.get('avatar_href')
        avatar_name = js.get('avatar_name')
        createTime = js.get('createTime')
        shortcode = js.get('shortcode')
        return render_to_response('ins/video.html', {
            'videoUrl': videoUrl,
            'jpgUrl': jpgUrl,
            'desc': desc,
            'avatar_url': avatar_url,
            'avatar_href': avatar_href,
            'avatar_name': avatar_name,
            'createTime': createTime,
            'short_code': shortcode
        })


def _get_redis_task(key):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    return r.get(key)


def _write_redis_status(key, content):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    r.set(key, content)


def donate(request):
    return render_to_response('ins/donate.html', {})


# https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/sh0.08/e35/p640x640/23421548_158659254868854_1840004499737935872_n.jpg 640w,https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/sh0.08/e35/p750x750/23421548_158659254868854_1840004499737935872_n.jpg 750w,https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/e35/23421548_158659254868854_1840004499737935872_n.jpg 1080w