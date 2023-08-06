#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import configparser
import requests
import argparse

STATUS = 'http://172.16.154.130/cgi-bin/rad_user_info'
PORTAL = 'http://172.16.154.130:69/cgi-bin/srun_portal'


# UDP_PORT1 = ('172.16.154.130', 3338)
# UDP_PORT2 = ('172.16.154.130', 4338)


def init():
    username = None
    password = None
    cf = configparser.ConfigParser()
    if os.path.isfile('config.ini'):
        cf.read("config.ini")
        username = cf.get("srun", "username")
        password = cf.get("srun", "password")
    parser = argparse.ArgumentParser(description='河南工业大学校园网登陆器')
    parser.add_argument('--user', '-u', type=str, help='username')
    parser.add_argument('--passwd', '-p', type=str, help='password')
    args = parser.parse_args()
    input_username = args.user
    input_password = args.passwd
    if input_username is None and input_password is None:
        if username is None or password is None:
            print("本地文件格式错误")
            sys.exit(0)

    elif input_username is None or input_password is None:
        print("必须同时输入username和password")
        sys.exit(0)
    else:
        username = input_username
        password = input_password
        if not cf.has_section("srun"):
            cf.add_section("srun")
        cf.set("srun", "username", username)
        cf.set("srun", "password", password)
        cf.write(open("config.ini", "w"))
    print("使用账号 %s 登陆中..." % username)
    return username, password


def request(url, data=None):
    r = None
    if data:
        r = requests.post(url, data=data)
    else:
        r = requests.get(url)
    return r.text


# def request(url, data=None):
#     with urlopen(url, data) as f:
#         return f.read().decode()


def username_encrypt(username):
    result = '{SRUN3}\r\n'
    return result + ''.join([chr(ord(x) + 4) for x in username])


def password_encrypt(password, key='1234567890'):
    result = list()
    for i in range(len(password)):
        ki = ord(password[i]) ^ ord(key[len(key) - i % len(key) - 1])
        _l = chr((ki & 0x0F) + 0x36)
        _h = chr((ki >> 4 & 0x0F) + 0x63)
        if i % 2 == 0:
            result.extend((_l, _h))
        else:
            result.extend((_h, _l))
    return ''.join(result)


def http_keep_login(username, password):
    e_username = username_encrypt(username)
    e_password = password_encrypt(password)
    post_data = {
        'action': 'login',
        'username': e_username,
        'password': e_password,
        'ac_id': 1,
        'drop': 0,
        'pop': 1,
        'type': 10,
        'n': 117,
        'mbytes': 0,
        'minutes': 0,
    }
    count = 0
    while True:
        res = request(STATUS)
        if res.startswith('not_online'):
            print('...')
            req = request(PORTAL, post_data)
            if req.startswith('login_ok') or req.startswith(
                    'login_error#E2620') or req.startswith(
                'ip_already_online_error'):  # You are already online.
                print('Login OK')
                sys.exit(0)
            elif 'BAS respond timeout' in req:
                if post_data['ac_id'] == 1:
                    post_data['ac_id'] = 2
                else:
                    post_data['ac_id'] = 1
            else:
                print(res)
            count += 1
            if count > 5:
                print("登录超时...")
                sys.exit(0)
            time.sleep(2)
        else:
            print(res)
            sys.exit(0)

def login():
    u, p = init()
    http_keep_login(u, p)


if __name__ == '__main__':
    login()
