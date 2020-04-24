#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: lab
@file: __init__.py.py
@time: 2019/3/25 16:29
@desc:
'''
import mitmproxy
from mitmproxy import http
from mitmproxy import ctx
from mitmproxy import websocket,tcp
import cmd
import os


from ctrip_cookie_pool import redis_client

URL = "https://hotels.ctrip.com/international/tool/AjaxHotelList.aspx"

redis = redis_client.RedisClient()

def websocket_message( flow: mitmproxy.websocket.WebSocketFlow):
    pass


def tcp_message(flow: mitmproxy.tcp.TCPFlow):
    """
        A TCP connection has received a message. The most recent message
        will be flow.messages[-1]. The message is user-modifiable.
    """
    pass


def modify(chunks):
    """
    chunks is a generator that can be used to iterate over all chunks.
    """
    for chunk in chunks:
        yield chunk.replace("foo", "bar")


def responseheaders(flow):
    # flow.response.stream = modify
    flow.response.stream = True


def request(flow: http.HTTPFlow):
    # redirect to different host
    process_request(flow)


def response(flow: http.HTTPFlow):
    pass


def responseheaders(flow):
    """
    Enables streaming for all responses.
    This is equivalent to passing `--set stream_large_bodies=1` to mitmproxy.
    """
    flow.response.stream = True


def websocket_error(flow: mitmproxy.websocket.WebSocketFlow):
    """
        A websocket connection has had an error.
    """
    pass


def process_request(flow):
    print("process_request")
    # print(flow.request.url)
    try:
        url = flow.request.url
        if url == URL:
            headers = flow.request.headers
            cookie = headers.get("cookie")
            if cookie:
                ctx.log.info(' cookie is:' + cookie)
                save_cookie(cookie)
    except Exception as e:
        ctx.log.info("error is " + str(e))


def save_cookie(cookie):
    # with open("cookie.txt", "w") as f:
    #     f.write(cookie)
    redis.add(cookie)

if __name__ == '__main__':
    cmd.Cmd()
    os.system("mitmdump -k -s mitproxy.py  --set stream_websockets=true")
