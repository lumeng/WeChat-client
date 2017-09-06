#!/usr/bin/env python3
# Summary: WeChat (https://wx.qq.com/) client in implemented in Python 3.
# Original version implemented in Python 2: http://blog.csdn.net/lin3p/article/details/51925700
# Meng Lu <lumeng.dev@gmail.com>
#
# References:
# * https://docs.python.org/3/library/urllib.request.html
# * https://docs.python.org/3/library/time.html
# * https://stackoverflow.com/questions/23118249/whats-the-difference-between-request-payload-vs-form-data-as-seen-in-chrome

import os

import sys

import re

import time

from PIL import Image

import urllib

import urllib.parse

# urllib2 or urlib.request: https://stackoverflow.com/questions/41650533\
# /cant-install-urllib2-for-python-2-7
# If using Python 2.*
# import urllib2
# If using Python 3.*
import urllib.request

# https://stackoverflow.com/questions/9857677/python-3-2-wont-import-cookielib
# If using Python 2.*
# import cookielib
# If using Python 3.*
import http.cookiejar

uuid = ''
tip = 0
image_path = os.path.join(os.getcwd(), "weixin_login_QR_code.jpg")


def get_uuid():
    global uuid
    url = 'https://login.weixin.qq.com/login'
    params = {
        'appid': 'wx782c26e4c19acffb',
        'redirect_uri':
            'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
        'fun': 'new',
        'lang': 'en_US',
        '_': int(time.time())
    }
    data = urllib.parse.urlencode(params).encode("utf-8")

    req = urllib.request.Request(url)

    with urllib.request.urlopen(req, data=data) as f:
        resp = f.read()
        regex = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+)"'
        matches = re.search(regex, resp.decode("utf-8"))
        code = matches.group(1)
        uuid = matches.group(2)

        if code == '200':
            return True
        return False


def get_qr_code():
    url = 'https://login.weixin.qq.com/qrcode/' + uuid
    params = {
        't': 'webwx',
        '_': int(time.time())
    }

    data = urllib.parse.urlencode(params).encode("utf-8")

    req = urllib.request.Request(url)

    with urllib.request.urlopen(req, data=data) as f:
        qr_file = open(image_path, 'wb')

        resp = f.read()
        qr_file.write(resp)
        qr_file.close()
        time.sleep(1)
        os.system('open %s' % image_path)

        print('Scan to log in to WeChat. Log in on phone to use WeChat on Web')


def is_logged_in():
    url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login'
    params = {
        'tip': tip,
        'uuid': uuid,
        '_': int(time.time())
    }
    data = urllib.parse.urlencode(params).encode("utf-8")

    req = urllib.request.Request(url)

    with urllib.request.urlopen(req, data=data) as f:
        resp = f.read()
        print(resp)
        regex = r'window.code=(\d+)'
        matches = re.search(regex, resp.decode("utf-8"))
        code = matches.group(1)
        print(code)
        if code == '201':
            print('Scan QR code successfully!')
        elif code == '200':
            print('Logging in...')
        elif code == '408':
            print('Login Timeout!')

    return code


def main():

    # Get the current cookie.
    cookie = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    # then for all requests
    urllib.request.install_opener(cookie)

    if not get_uuid():
        print('Fail to get an UUID for logging into WeChat. Quit.')
        return None

    get_qr_code()
    time.sleep(1)

    while is_logged_in() != '200':
        pass

    os.remove(image_path)
    print('Login successfully!')


def send_message():
    url = 'https://web.wechat.com/cgi-bin/mmwebwx-bin/webwxsendmsg'
    params = {

        'BaseRequest': {
            'Uin': '866402043',
            'Sid': "uyi2W3wkny9Nclbs",
            'Skey': "@crypt_bf880690_4dc413727fb95edeb9b01093c76e2049"
        },
        'DeviceID': "e796860397176700",
        'Sid': "uyi2W3wkny9Nclbs",
        'Skey': "@crypt_bf880690_4dc413727fb95edeb9b01093c76e2049",
        'Uin': '866402043',
        'Msg': {
            'Type': 1,
            'Content': "Test"
        },
        'ClientMsgId': "15045872490880266",
        'Content': "Test",
        'FromUserName':
            "@b1772435c48749d795124e7925b379bb607665b5ebbb162ec1a144ff5ae1affc",
        'LocalID': "15045872490880266",
        'ToUserName':
            "@@268cf4c8f5e5ba8af562599fe681a0827b829394959c7d3ee527edc9c8fbc916",
        'Type': 1,
        'Scene': 0
    }


if __name__ == '__main__':
    print('Welcome to WeChat')
    print('Please click Enter key to continue ...')
    main()
# END
