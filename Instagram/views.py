# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
import json
from models import Ins
import requests
from GithubTrendingDjango import _redis

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
        return render(redisData)
    else:
        # _write_redis_status('ins',url)
        r.rpush('ins',url)
        redisData = None
        # print  _get_redis_task(url)
        while redisData == None:
            redisData = _get_redis_task(url)
            print redisData
            if redisData is not None:
                return render(redisData)
        # s = requests.get(url,verify=False)
                
def render(redisData):
    js = json.loads(redisData)
    avatar_url = js.get('graphql').get('shortcode_media').get('owner').get('profile_pic_url')
    avatar_href = 'https://www.instagram.com/%s/' % js.get('graphql').get('shortcode_media').get('owner').get('username')
    avatar_name = js.get('graphql').get('shortcode_media').get('owner').get('username')
    edge_sidecar_to_children = js.get('graphql').get('shortcode_media').get('edge_sidecar_to_children')
    if edge_sidecar_to_children == None:
        display_resources = js.get('graphql').get('shortcode_media').get('display_resources')
    imgs = []
    if edge_sidecar_to_children:
        edges = edge_sidecar_to_children.get('edges')
        for edge in edges:
            node = edge.get('node')
            display_resources = node.get('display_resources')
            img = display_resources[len(display_resources) - 1].get('src')
            imgs.append(img)
    else:
        imgs.append(display_resources[len(display_resources)-1].get('src'))
        
    # print a.url
    return render_to_response('ins/index.html', {
        'avatar_name':avatar_name,
        'avatar_url': avatar_url,
        'avatar_href': avatar_href,
        'imgs': imgs
    })

def _get_redis_task(key):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    return r.get(key)

def _write_redis_status(key,content):
    _redis_ = _redis.RedisC()
    r = _redis_._redis_()
    r.set(key,content)

def donate(request):
    return render_to_response('ins/donate.html',{})

# https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/sh0.08/e35/p640x640/23421548_158659254868854_1840004499737935872_n.jpg 640w,https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/sh0.08/e35/p750x750/23421548_158659254868854_1840004499737935872_n.jpg 750w,https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/e35/23421548_158659254868854_1840004499737935872_n.jpg 1080w